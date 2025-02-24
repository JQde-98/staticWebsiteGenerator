import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, extract_markdown_images, extract_markdown_links

class TestHTMLnode(unittest.TestCase):
    def test_prop_to_html(self):
        dict = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode('p', 'this is a test node', props=dict)

        node.props_to_html()

    def test_prop_to_html2(self):
        dict = {}
        node = HTMLNode('p', 'this is a test node', None, dict)
        
        node.props_to_html()

    def test_prop_to_html3(self):
        dict = {
            "href": "https://www.google.com",
            "target": "_blank",
            "testkey": "testvalue",
            "testkey2": "testvalue2",
        }
        node = HTMLNode('p', 'this is a test node', None, dict)
        
        node.props_to_html()

    def test_eq2(self):
        node = HTMLNode("p", "this is a test node")
        node2 = HTMLNode("p", "this is a test node")
        self.assertEqual(node, node2)

    def test_noteq(self):
        node = HTMLNode("p", "this is a test node")
        node2 = HTMLNode("p", "THIS is a test node")
        self.assertNotEqual(node, node2)

    def test_empty_props(self):
        node = HTMLNode("p", "test", props={})
        self.assertEqual(node.props_to_html(), "")

    def test_none_props(self):
        node = HTMLNode("p", "test", props=None)
        self.assertEqual(node.props_to_html(), "")
    
    def test_props_special_characters(self):
        props = {
            "src": "http://example.com?a=1&b=2",
            "title": "Quotes \" and apostrophes '"
        }

        node = HTMLNode("img", props=props)
        expected = ' src="http://example.com?a=1&b=2" title="Quotes \" and apostrophes \'"'
        self.assertEqual(node.props_to_html(), expected)

    def test_props_more_special_characters(self):
        props = {
            "data-test": "<script>alert('hello')</script>",
            "title": "Multiple lines \n and \t tabs"
        }

        node = HTMLNode("div", props=props)
        expected = ' data-test="<script>alert(\'hello\')</script>" title="Multiple lines \n and \t tabs"'
        self.assertEqual(node.props_to_html(), expected)

    def test_props_ordering(self):
        # Create two nodes with same props in different order
        props1 = {
            "href": "https://example.com",
            "class": "link",
        }

        props2 = {
            "class": "link",
            "href": "https://example.com",
        }
    
        node1 = HTMLNode("a", props=props1)
        node2 = HTMLNode("a", props=props2)
    
        # Do they produce the same HTML?
        self.assertEqual(node1.props_to_html(), node2.props_to_html())

    def test_to_html_leafnode(self):
        node = LeafNode("p", "Hello World!")
        self.assertEqual(node.to_html(), "<p>Hello World!</p>")

    def test_to_html_leafnode_with_props(self):
        node = LeafNode("a", "Click here!", props={"href": "https://example.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://example.com\">Click here!</a>")

    def test_to_html_leafnode_notag(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_to_html_leafnode_novalue(self):
        with self.assertRaises(ValueError):
            node = LeafNode("p", None)
            node.to_html()
        
    def test_to_html_parentNode(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"), 
                LeafNode(None, "Normal text"), 
                LeafNode("i", "italic text"), 
                LeafNode(None, "Normal text"),
                ],
            )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_to_html_valueErrorTag(self):
        with self.assertRaises(ValueError):
            node = ParentNode(None, [LeafNode("b", "Bold text"), LeafNode(None, "Normal text"),])
            node.to_html()

    def test_to_html_valueErrorChildren(self):
        with self.assertRaises(ValueError):
            node = ParentNode("b", None)
            node.to_html()

    def test_to_html_nested_parentNode(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"), 
                LeafNode(None, "Normal text"), 
                LeafNode("i", "italic text"), 
                ParentNode(
                "p",
                [
                    LeafNode("b", "Bold text"), 
                    LeafNode(None, "Normal text"), 
                    LeafNode("i", "italic text"), 
                    ],
                ),
                ],
            )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i><p><b>Bold text</b>Normal text<i>italic text</i></p></p>")  

    def test_parentNode_with_props(self):
        node = ParentNode(
            "div",
            [LeafNode("p", "Hello")],
            {"class": "greeting", "id": "welcome"}
        )
        self.assertEqual(node.to_html(), '<div class="greeting" id="welcome"><p>Hello</p></div>')

    def test_deeply_nested_parentNode(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "section",
                    [
                        ParentNode(
                            "article",
                            [LeafNode("p", "Deep nest")]
                        )
                    ]
                )
            ]
        )
        self.assertEqual(node.to_html(), "<div><section><article><p>Deep nest</p></article></section></div>")

    def test_empty_children_list(self):
        # Different from None children - should NOT raise ValueError
        node = ParentNode("div", [])
        self.assertEqual(node.to_html(), "<div></div>")

    def test_extract_basic_image(self):
        text = "![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_multiple_images(self):
        text = "![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_basic_link(self):
        text = "[to boot dev](https://www.boot.dev)"
        expected = [("to boot dev", "https://www.boot.dev")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_extract_multiple_links(self):
        text = "[boot.dev](https://www.boot.dev) and [youtube](https://youtube.com)"
        expected = [
            ("boot.dev", "https://www.boot.dev"),
            ("youtube", "https://youtube.com")
        ]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_empty_text(self):
        self.assertEqual(extract_markdown_images(""), [])
        self.assertEqual(extract_markdown_links(""), [])

    def test_text_with_no_matches(self):
        text = "This is just plain text without any markdown"
        self.assertEqual(extract_markdown_images(text), [])

    def test_mixed_content(self):
        text = "Here's a ![cute cat](https://pics.com/cat.jpg) and a [link to dogs](https://dogs.com)"
        self.assertEqual(
            extract_markdown_images(text),
            [("cute cat", "https://pics.com/cat.jpg")]
        )
        self.assertEqual(
            extract_markdown_links(text),
            [("link to dogs", "https://dogs.com")]
        )

    def test_special_characters_in_url(self):
        text = "![test](https://example.com/path?param=1&other=2) [complex link](https://api.com/path?q=test&page=1#section)"
        self.assertEqual(
            extract_markdown_images(text),
            [("test", "https://example.com/path?param=1&other=2")]
        )
        self.assertEqual(
            extract_markdown_links(text),
            [("complex link", "https://api.com/path?q=test&page=1#section")]
        )

    def test_multiline_content(self):
        text = """
        First line with ![image1](https://test.com/1.jpg)
        Second line with [link1](https://test.com/page1)
        Third line with ![image2](https://test.com/2.jpg)
        """
        self.assertEqual(
            extract_markdown_images(text),
            [
                ("image1", "https://test.com/1.jpg"),
                ("image2", "https://test.com/2.jpg")
            ]
        )
        self.assertEqual(
            extract_markdown_links(text),
            [("link1", "https://test.com/page1")]
        )
    
    def test_adjacent_links_and_images(self):
        text = "![img1](url1)![img2](url2)[link1](url3)[link2](url4)"
        self.assertEqual(
            extract_markdown_images(text),
            [("img1", "url1"), ("img2", "url2")]
        )
        self.assertEqual(
            extract_markdown_links(text),
            [("link1", "url3"), ("link2", "url4")]
        )

    def test_empty_alt_text_and_urls(self):
        text = "![](https://example.com) [](https://example.com)"
        self.assertEqual(
            extract_markdown_images(text),
            [("", "https://example.com")]
        )
        self.assertEqual(
            extract_markdown_links(text),
            [("", "https://example.com")]
        )


if __name__ == "__main__":
    unittest.main()