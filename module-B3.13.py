class Tag:

    def __init__(self, tag, is_single=False, klass=None, **kwargs):
        self.tag = tag
        self.text = ""
        self.attributes = {}
        self.is_single = is_single
        self.children = []

        if klass is not None:
            self.attributes["klass"] = "".join(klass)

        for attr, val in kwargs.items():
            if "_" in attr:
                attr = attr.replace("_", "-")

            self.attributes[attr] = val

    def __enter__(self):
        return self

    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __exit__(self, *args, **kwargs):
        pass


    def __str__(self):
        attributes = []
        for attr, val in self.attributes.items():
            attributes.append('{}="{}"'.format(attr, val))
        attributes = "".join(attributes)

        if len(self.children) > 0:
            opening = "<{}{}>".format(self.tag, attributes)

            if self.text:
                internal = "{}".format(self.text)
            else:
                internal = ""

            for child in self.children:
                internal += str(child)
            ending = "</{}>".format(self.tag)

            return opening + internal + ending

        else:
            if self.is_single:
                return "<{} {}/>".format(self.tag, attributes)
            else:
                return "<{} {}>{}</{}>".format(self.tag, attributes, self.text, self.tag)


class HTML:
    def __init__(self, output=None):
        self.output = output
        self.children = []

    def __enter__(self):
        return self

    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __exit__(self, *args, **kwargs):
        if self.output is not None:
            with open(self.output, "w") as f:
                f.write(str(self))
        else:
            print(self)

    def __str__(self):
        html = "<html>\n"
        for child in self.children:
            html += str(child)
        html += "\n<\html>"

        return html


class TopLevelTag:
    def __init__(self, tag, **kwargs):
        self.tag = tag
        self.children = []

    def __enter__(self):
        return self

    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __exit__(self, *args, **kwargs):
        pass

    def __str__(self):
        html = "<{}>\n".format(self.tag)

        for child in self.children:
            html += str(child)
        html +="\n<\{}>".format(self.tag)

        return html


if __name__ == "__main__":
    with HTML(output=None) as doc:
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "hello"
                head += title
            doc += head

        with TopLevelTag("body") as body:
            with Tag("h1", klass=("main-text",)) as h1:
                h1.text = "Test"
                body += h1

            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                with Tag("p") as paragraph:
                    paragraph.text = "another test"
                    div += paragraph

                with Tag("img", is_single=True, src="/icon.png") as img:
                    div += img

                body += div

            doc += body

