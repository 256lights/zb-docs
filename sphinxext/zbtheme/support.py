from pygments.style import Style
from pygments.token import (
    Comment,
    Generic,
    Keyword,
    Name,
    Number,
    Operator,
    Punctuation,
    String,
)


class ZB(Style):
    background_color = "var(--color-amber-50)"  # bg-amber-50

    styles = {
        Comment: "italic var(--color-amber-800)",     # text-amber-800
        Keyword: "bold var(--color-cyan-800)",        # text-cyan-800
        Name.Builtin: "bold var(--color-cyan-800)",   # text-cyan-800
        Name.Tag: "bold var(--color-cyan-800)",       # text-cyan-800
        Number: "var(--color-red-800)",               # text-red-800
        Operator.Word: "bold var(--color-cyan-800)",  # text-cyan-800
        Punctuation: "bold",
        String: "var(--color-lime-700)",              # text-lime-700

        # bg-red-50 text-red-950
        Generic.Deleted: "bg:var(--color-red-50) var(--color-red-950)",
        # bg-lime-50 text-lime-950
        Generic.Inserted: "bg:var(--color-lime-50) var(--color-lime-950)",
    }
