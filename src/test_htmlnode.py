import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_none(self):
        node = HTMLNode("p", "This is a test")
        self.assertEqual(node.props_to_html(), "")
    
    def test_props_to_html_link(self):
        node = HTMLNode("a", "This is a link", None, {
            "href": "https://www.google.com",
            "target": "_blank"
        })
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')
    
    def test_props_to_html_image(self):
        node = HTMLNode("img", None, None, {
            "src": "img_girl.jpg",
            "alt": "Girl in a jacket",
            "width": "500",
            "height": "600"
        })
        self.assertEqual(node.props_to_html(), ' src="img_girl.jpg" alt="Girl in a jacket" width="500" height="600"')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_href(self):
        node = LeafNode("a", "Click me!", {
            "href": "https://www.google.com"
        })
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_empty_tag(self):
        node = LeafNode(None, "testing")
        self.assertEqual("testing", node.to_html())

    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )


    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_children(self):
        grandgrandchild_node_1 = LeafNode("tag1", "ggchild1")     
        grandgrandchild_node_2 = LeafNode("tag2", "ggchild2")
        grandgrandchild_node_3 = LeafNode("tag3", "ggchild3")
        grandgrandchild_node_4 = LeafNode("tag4", "ggchild4")
        grandgrandchild_node_5 = LeafNode("tag5", "ggchild5")
        grandchild_node_1 = ParentNode("gctag1", [grandgrandchild_node_1, grandgrandchild_node_2, grandgrandchild_node_3])
        grandchild_node_2 = ParentNode("gctag2", [grandgrandchild_node_4, grandgrandchild_node_5])

        parent_node = ParentNode("tag", [grandchild_node_1, grandchild_node_2])

        self.assertEqual(
            parent_node.to_html(),
            "<tag><gctag1><tag1>ggchild1</tag1><tag2>ggchild2</tag2><tag3>ggchild3</tag3></gctag1><gctag2><tag4>ggchild4</tag4><tag5>ggchild5</tag5></gctag2></tag>"
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )

if __name__ == "__main__":
    unittest.main()