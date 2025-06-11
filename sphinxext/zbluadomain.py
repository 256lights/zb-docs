# Adapted from https://github.com/boolangery/sphinx-luadomain/blob/b2430927a181fbac1e999e40b404a58c99e6e0d3/sphinxcontrib/luadomain.py
# SPDX-License-Identifier: BSD-3-Clause

from typing import Any, Dict, List, NamedTuple, Tuple, Optional, override, TYPE_CHECKING

from docutils import nodes
from docutils.parsers.rst import Directive, directives
from sphinx import addnodes
from sphinx.application import Sphinx
from sphinx.builders import Builder
from sphinx.directives import ObjectDescription
from sphinx.domains import Domain, ObjType, Index
from sphinx.environment import BuildEnvironment
from sphinx.locale import get_translation
from sphinx.roles import XRefRole
from sphinx.util import logging
from sphinx.util.docfields import Field, TypedField
from sphinx.util.nodes import make_refnode

if TYPE_CHECKING:
    from sphinx.writers.latex import LaTeXTranslator
    from sphinx.writers.html5 import HTML5Translator

logger = logging.getLogger(__name__)
_ = get_translation('zbluadomain')

class _LuaSignature(NamedTuple):
    name_prefix: Optional[str]
    name: str
    arg_list: Optional[str] = None
    table_params: bool = False

def _find_any(s: str, charset: str) -> int:
    for i, c in enumerate(s):
        if c in charset:
            return i
    return -1

def _parse_signature(s: str) -> _LuaSignature:
    arg_start = _find_any(s, '({')
    if arg_start >= 0:
        arg_pair = (s[arg_start], s[-1])
        if arg_pair not in (('(', ')'), ('{', '}')):
            raise ValueError('lua function signature: closing parenthesis does not match')
        args = s[arg_start+1:-1]
        table_params = arg_pair[0] == '{'
    else:
        args = None
        table_params = False
    fullname = s[:arg_start].rstrip() if arg_start >= 0 else s
    dot_index = fullname.rfind('.')
    if dot_index == len(fullname) - 1:
        raise ValueError('lua function signature: function name cannot end in dot')
    if dot_index < 0:
        return _LuaSignature(None, fullname, args, table_params)
    return _LuaSignature(fullname[:dot_index+1], fullname[dot_index+1:], args, table_params)

class desc_table_parameter_list(nodes.Part, nodes.Inline, nodes.FixedTextElement):
    child_text_separator = ', '

    def astext(self) -> str:
        return '{' + super().astext() + '}'

class LuaObject(ObjectDescription):
    option_spec = {
        'noindex': directives.flag,
        'module': directives.unchanged,
    }
    doc_field_types = [
        TypedField('parameter', label=_('Parameters'),
                   names=('param', 'parameter', 'arg', 'argument', 'keyword', 'kwarg', 'kwparam'),
                   typerolename='class', typenames=('type',)),
        Field('returnvalue', label=_('Returns'), has_arg=False,
              names=('returns', 'return')),
        Field('returntype', label=_('Return type'), has_arg=False,
              names=('rtype',), bodyrolename='class'),
    ]

    allow_nesting = False

    def needs_arg_list(self) -> bool:
        return False

    @override
    def handle_signature(self, sig, signode) -> Tuple[str, Optional[str]]:
        name_prefix, name, arg_list, table_params = _parse_signature(sig)

        # determine module and class name (if applicable), as well as full name
        modname = self.options.get(
            'module', self.env.ref_context.get('lua:module'))
        class_name = self.env.ref_context.get('lua:class')
        if class_name:
            add_module = False
            if name_prefix and name_prefix.startswith(class_name):
                fullname = name_prefix + name
                # class name is given again in the signature
                name_prefix = name_prefix[len(class_name):].lstrip('.')
            elif name_prefix:
                # class name is given in the signature, but different
                # (shouldn't happen)
                fullname = class_name + '.' + name_prefix + name
            else:
                # class name is not given in the signature
                fullname = class_name + '.' + name
        else:
            add_module = True
            if name_prefix:
                class_name = name_prefix.rstrip('.')
                fullname = name_prefix + name
            else:
                class_name = ''
                fullname = name

        signode['module'] = modname
        signode['class'] = class_name
        signode['fullname'] = fullname

        if name_prefix:
            signode += addnodes.desc_addname(name_prefix, name_prefix)
        elif add_module:
            modname = self.options.get('module', self.env.ref_context.get('lua:module'))
            if modname:
                node_text = modname + '.'
                signode += addnodes.desc_addname(node_text, node_text)

        signode += addnodes.desc_name(name, name)
        if not arg_list:
            if self.needs_arg_list():
                # for callables, add an empty parameter list
                signode += addnodes.desc_parameterlist()
            return fullname, name_prefix

        param_list = desc_table_parameter_list() if table_params else addnodes.desc_parameterlist()
        stack: List[nodes.Element] = [param_list]
        try:
            for argument in arg_list.split(','):
                argument = argument.strip()
                ends_open = 0
                ends_close = 0
                while argument.startswith('['):
                    stack.append(addnodes.desc_optional())
                    stack[-2] += stack[-1]
                    argument = argument[1:].strip()
                while argument.startswith(']'):
                    stack.pop()
                    argument = argument[1:].strip()
                while argument.endswith(']') and not argument.endswith('[]'):
                    ends_close += 1
                    argument = argument[:-1].strip()
                while argument.endswith('['):
                    ends_open += 1
                    argument = argument[:-1].strip()
                if argument:
                    stack[-1] += addnodes.desc_parameter(argument, argument)
                while ends_open:
                    stack.append(addnodes.desc_optional())
                    stack[-2] += stack[-1]
                    ends_open -= 1
                while ends_close:
                    stack.pop()
                    ends_close -= 1
            if len(stack) != 1:
                raise IndexError
        except IndexError:
            # if there are too few or too many elements on the stack, just give up
            # and treat the whole argument list as one argument, discarding the
            # already partially populated paramlist node
            param_list = desc_table_parameter_list() if table_params else addnodes.desc_parameterlist()
            param_list += addnodes.desc_parameter(arg_list, arg_list)
        signode += param_list

        return fullname, name_prefix

    def get_index_text(self, modname: Optional[str], name: Tuple[str, Optional[str]]) -> str:
        raise NotImplementedError('must be implemented in subclasses')

    @override
    def add_target_and_index(self, name: Tuple[str, Optional[str]], sig, signode):
        modname: Optional[str] = self.options.get('module', self.env.ref_context.get('lua:module'))
        fullname = (modname and modname + '.' or '') + name[0]

        if fullname not in self.state.document.ids:
            signode['names'].append(fullname)
            signode['ids'].append(fullname)
            signode['first'] = (not self.names)
            self.state.document.note_explicit_target(signode)
            objects = self.env.domaindata['lua']['objects']
            if fullname in objects:
                self.state_machine.reporter.warning(
                    'duplicate object description of %s, ' % fullname +
                    'other instance in ' +
                    self.env.doc2path(objects[fullname][0]) +
                    ', use :noindex: for one of them',
                    line=self.lineno)
            objects[fullname] = (self.env.docname, self.objtype)

        indextext = self.get_index_text(modname, name)
        if indextext:
            self.indexnode['entries'].append(('single', indextext,
                                              fullname, '', None))


class LuaFunction(LuaObject):
    @override
    def needs_arg_list(self):
        return True

    @override
    def get_index_text(self, modname, name) -> str:
        if not modname:
            return _('%s() (built-in function)') % name[0]
        return _('%s() (in module %s)') % (name[0], modname)


class LuaData(LuaObject):
    @override
    def get_index_text(self, modname, name) -> str:
        if not modname:
            return _('%s() (built-in variable)') % name[0]
        return _('%s() (in module %s)') % (name[0], modname)


class LuaModule(Directive):
    """
    Directive to mark description of a new module.
    """

    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        'platform': lambda x: x,
        'synopsis': lambda x: x,
        'noindex': directives.flag,
        'deprecated': directives.flag,
    }

    @override
    def run(self):
        env = self.state.document.settings.env
        modname = self.arguments[0].strip()
        no_index = 'noindex' in self.options
        env.ref_context['lua:module'] = modname
        ret = []
        if not no_index:
            env.domaindata['lua']['modules'][modname] = \
                (env.docname, self.options.get('synopsis', ''),
                 self.options.get('platform', ''), 'deprecated' in self.options)
            # make a duplicate entry in 'objects' to facilitate searching for
            # the module in LuaDomain.find_obj()
            env.domaindata['lua']['objects'][modname] = (env.docname, 'module')
            target_node = nodes.target('', '', ids=['module-' + modname],
                                      ismod=True)
            self.state.document.note_explicit_target(target_node)
            # the platform and synopsis aren't printed; in fact, they are only
            # used in the modindex currently
            ret.append(target_node)
            indextext = _('%s (module)') % modname
            inode = addnodes.index(entries=[('single', indextext,
                                             'module-' + modname, '', None)])
            ret.append(inode)
        return ret


class LuaCurrentModule(Directive):
    """
    This directive is just to tell Sphinx that we're documenting
    stuff in module foo, but links to module foo won't lead here.
    """

    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {}

    @override
    def run(self):
        env = self.state.document.settings.env
        modname = self.arguments[0].strip()
        if modname == 'None':
            env.ref_context.pop('lua:module', None)
        else:
            env.ref_context['lua:module'] = modname
        return []


class LuaXRefRole(XRefRole):
    @override
    def process_link(self, env, refnode, has_explicit_title, title, target):
        refnode['lua:module'] = env.ref_context.get('lua:module')
        refnode['lua:class'] = env.ref_context.get('lua:class')
        if not has_explicit_title:
            title = title.lstrip('.')  # only has a meaning for the target
            target = target.lstrip('~')  # only has a meaning for the title
            # if the first character is a tilde, don't display the module/class
            # parts of the contents
            if title[0:1] == '~':
                title = title[1:]
                dot = title.rfind('.')
                if dot != -1:
                    title = title[dot + 1:]
        return title, target


class LuaModuleIndex(Index):
    """
    Index subclass to provide the Lua module index.
    """

    name = 'modindex'
    localname = _('Lua Module Index')
    shortname = _('modules')

    @override
    def generate(self, docnames = None):
        content: Dict[str, List] = {}
        # list of prefixes to ignore
        ignores = self.domain.env.config['modindex_common_prefix']
        ignores = sorted(ignores, key=len, reverse=True)
        # list of all modules, sorted by module name
        modules = sorted(self.domain.data['modules'].items(),
                         key=lambda x: x[0].lower())
        # sort out collapsable modules
        prev_modname = ''
        num_top_levels = 0
        for modname, (docname, synopsis, platforms, deprecated) in modules:
            if docnames and docname not in docnames:
                continue

            for ignore in ignores:
                if modname.startswith(ignore):
                    modname = modname[len(ignore):]
                    stripped = ignore
                    break
            else:
                stripped = ''

            # we stripped the whole module name?
            if not modname:
                modname, stripped = stripped, ''

            entries = content.setdefault(modname[0].lower(), [])

            package = modname.split('.')[0]
            if package != modname:
                # it's a submodule
                if prev_modname == package:
                    # first submodule - make parent a group head
                    if entries:
                        entries[-1][1] = 1
                elif not prev_modname.startswith(package):
                    # submodule without parent in list, add dummy entry
                    entries.append([stripped + package, 1, '', '', '', '', ''])
                subtype = 2
            else:
                num_top_levels += 1
                subtype = 0

            qualifier = deprecated and _('Deprecated') or ''
            entries.append([stripped + modname, subtype, docname,
                            'module-' + stripped + modname, platforms,
                            qualifier, synopsis])
            prev_modname = modname

        # apply heuristics when to collapse modindex at page load:
        # only collapse if number of toplevel modules is larger than
        # number of submodules
        collapse = len(modules) - num_top_levels < num_top_levels

        # sort by first letter
        sorted_content = sorted(content.items())

        return sorted_content, collapse


class LuaDomain(Domain):
    name = 'lua'
    label = 'Lua'
    object_types = {
        'function': ObjType(_('function'), 'func', 'obj'),
        'data': ObjType(_('data'), 'data', 'obj'),
        'module': ObjType(_('module'), 'mod', 'obj'),
    }

    directives = {
        'function': LuaFunction,
        'data': LuaData,
        'module': LuaModule,
    }
    roles = {
        'data': LuaXRefRole(),
        'func': LuaXRefRole(fix_parens=True),
        'class': LuaXRefRole(),
        'const': LuaXRefRole(),
        'mod': LuaXRefRole(),
        'obj': LuaXRefRole(),
    }
    initial_data: Dict[str, Dict[str, Tuple[Any]]] = {
        'objects': {}, # fullname -> docname, objtype
        'modules': {}, # fullname -> docname, synopsis, platform, deprecated
    }
    indices = [LuaModuleIndex]

    @override
    def clear_doc(self, docname):
        for fullname, (fn, _objtype) in list(self.data['objects'].items()):
            if fn == docname:
                del self.data['objects'][fullname]
        for fullname, data in list(self.data['modules'].items()):
            if data[0] == docname:
                del self.data['modules'][fullname]

    @override
    def merge_domaindata(self, docnames, otherdata):
        for fullname, (fn, objtype) in list(self.data['objects'].items()):
            if fn in docnames:
                self.data['objects'][fullname] = (fn, objtype)
        for modname, data in list(self.data['modules'].items()):
            if data[0] in docnames:
                self.data['modules'][modname] = data

    def find_obj(self, env: BuildEnvironment, modname: str, class_name: str, name: str, type: Optional[str],
                 search_mode: int = 0) -> List[Tuple[str, Any]]:
        """Find a Lua object for "name", perhaps using the given module
        and/or classname.  Returns a list of (name, object entry) tuples.
        """
        # skip parens
        if name[-2:] == '()':
            name = name[:-2]

        if not name:
            return []

        objects = self.data['objects']
        matches: List[Tuple[str, Any]] = []

        new_name = None

        # NOTE: searching for exact match, object type is not considered
        if name in objects:
            new_name = name
        elif type == 'mod':
            # only exact matches allowed for modules
            return []
        elif class_name and class_name + '.' + name in objects:
            new_name = class_name + '.' + name
        elif modname and modname + '.' + name in objects:
            new_name = modname + '.' + name
        elif modname and class_name and \
                modname + '.' + class_name + '.' + name in objects:
            new_name = modname + '.' + class_name + '.' + name
        # special case: object methods
        elif type in ('func', 'meth') and '.' not in name and \
                'object.' + name in objects:
            new_name = 'object.' + name

        if new_name is not None:
            matches.append((new_name, objects[new_name]))

        return matches

    @override
    def resolve_xref(self, env, fromdocname, builder, typ, target, node, contnode):
        modname = node.get('lua:module')
        class_name = node.get('lua:class')
        search_mode = 0
        matches = self.find_obj(env, modname, class_name, target,
                                typ, search_mode)
        if not matches:
            return None
        elif len(matches) > 1:
            logger.warning('more than one target found for cross-reference %r: %s',
                           target, ', '.join(match[0] for match in matches),
                           type='ref', subtype='lua', location=node)

        name, obj = matches[0]

        if obj[1] == 'module':
            return self._make_module_refnode(builder, fromdocname, name,
                                             contnode)
        else:
            return make_refnode(builder, fromdocname, obj[0], name,
                                contnode, name)

    @override
    def resolve_any_xref(self, env, fromdocname, builder, target, node, contnode):
        modname = node.get('lua:module')
        class_name = node.get('lua:class')
        results:  List[Tuple[str, nodes.reference]] = []

        # always search in "refspecific" mode with the :any: role
        matches = self.find_obj(env, modname, class_name, target, None, 1)
        for name, obj in matches:
            if obj[1] == 'module':
                results.append(('lua:mod',
                                self._make_module_refnode(builder, fromdocname,
                                                          name, contnode)))
            else:
                role = self.role_for_objtype(obj[1])
                assert role, 'missing role for ' + obj[1]
                results.append(('lua:' + role,
                                make_refnode(builder, fromdocname, obj[0], name,
                                             contnode, name)))
        return results

    def _make_module_refnode(self, builder: Builder, fromdocname: str, name: str, cont_node: nodes.Node) -> nodes.reference:
        # get additional info for modules
        docname, synopsis, platform, deprecated = self.data['modules'][name]
        title = name
        if synopsis:
            title += ': ' + synopsis
        if deprecated:
            title += _(' (deprecated)')
        if platform:
            title += ' (' + platform + ')'
        return make_refnode(builder, fromdocname, docname,
                            'module-' + name, cont_node, title)

    @override
    def get_objects(self):
        for modname, info in self.data['modules'].items():
            yield (modname, modname, 'module', info[0], 'module-' + modname, 0)
        for refname, (docname, type) in self.data['objects'].items():
            if type != 'module':  # modules are already handled
                yield (refname, refname, type, docname, refname, 1)

    @override
    def get_full_qualified_name(self, node) -> Optional[str]:
        modname = node.get('lua:module')
        class_name = node.get('lua:class')
        target = node.get('reftarget')
        if target is None:
            return None
        else:
            return '.'.join(filter(None, [modname, class_name, target]))


def visit_html_table_parameter_list(self: 'HTML5Translator', node: desc_table_parameter_list):
    self._visit_sig_parameter_list(node, addnodes.desc_parameter, '{', '}')


def depart_html_table_parameter_list(self: 'HTML5Translator', node: desc_table_parameter_list):
    self._depart_sig_parameter_list(node)


def visit_latex_table_parameter_list(self: 'LaTeXTranslator', node: desc_table_parameter_list):
    self.body.append(r'\{')
    self._visit_sig_parameter_list(node, addnodes.desc_parameter)


def depart_latex_table_parameter_list(self: 'LaTeXTranslator', node: desc_table_parameter_list):
    self.body.append(r'\}')


def setup(app: Sphinx):
    app.add_domain(LuaDomain)
    app.add_node(
        desc_table_parameter_list,
        html=(visit_html_table_parameter_list, depart_html_table_parameter_list),
        latex=(visit_latex_table_parameter_list, depart_latex_table_parameter_list),
    )
