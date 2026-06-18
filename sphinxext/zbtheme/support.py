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
    background_color = "#faf3e8"

    styles = {
        Comment: "italic #8f5902",
        Generic.Deleted: "#a40000",
        Generic.Inserted: "#00a000",
        Keyword: "bold #004461",
        Name.Builtin: "bold #004461",
        Name.Tag: "bold #004461",
        Number: "#990000",
        Operator.Word: "bold #004461",
        Punctuation: "bold",
        String: "#4e9a06",
    }
