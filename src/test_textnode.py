import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter
from htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_noteq(self):
        node = TextNode('this is a text node', TextType.ITALIC, "")
        node2 = TextNode('this is a test node', TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq2(self):
        node = TextNode('test test test', TextType.IMAGE, None)
        node2 = TextNode('test test test', TextType.IMAGE)
        self.assertEqual(node, node2)

    def test_noteq2(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_text_node_to_html_node_text(self):
        text_node = TextNode("Hello, world!", TextType.TEXT)
    
        html_node = text_node_to_html_node(text_node)
    
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "Hello, world!")
        self.assertEqual(html_node.props, None)

    def test_text_node_to_html_node_text2(self):
        text_node = TextNode("Hello, world!", TextType.BOLD)
    
        html_node = text_node_to_html_node(text_node)

        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Hello, world!")
        self.assertEqual(html_node.props, None)  

    def test_text_node_to_html_node_text3(self):
        text_node = TextNode("Hello, world!", TextType.ITALIC)
    
        html_node = text_node_to_html_node(text_node)

        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Hello, world!")
        self.assertEqual(html_node.props, None)    

    def test_text_node_to_html_node_text4(self):
        text_node = TextNode("Hello, world!", TextType.CODE)
    
        html_node = text_node_to_html_node(text_node)

        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Hello, world!")
        self.assertEqual(html_node.props, None)    

    def test_text_node_to_html_node_text5(self):
        text_node = TextNode("Click me!", TextType.LINK, "https://www.boot.dev")
    
        html_node = text_node_to_html_node(text_node)
    
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me!")
        self.assertEqual(html_node.props, {"href": "https://www.boot.dev"})           

    def test_text_node_to_html_node_text6(self):
        text_node = TextNode("My Cat", TextType.IMAGE, "https://cats.com/cat.png")
    
        html_node = text_node_to_html_node(text_node)

        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://cats.com/cat.png", "alt": "My Cat"})  

    def test_text_node_to_html_node_exception(self):
        text_node = TextNode("Hello, world!", TextType.TEXT)
        text_node.text_type = "invalid_type"
    
        with self.assertRaises(Exception):
            html_node = text_node_to_html_node(text_node)

    def test_delimiter(self):
        nodes = [TextNode("Hello `code` world", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" world", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_no_delimiters(self):
        nodes = [TextNode("Hello world", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [TextNode("Hello world", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_multiple_delimiters(self):
        nodes = [TextNode("Hello `code` and `more code`", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("more code", TextType.CODE),
            TextNode("", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_mismatched_delimiters(self):
        nodes = [TextNode("Hello `code", TextType.TEXT)]
        with self.assertRaises(Exception):
            split_nodes_delimiter(nodes, "`", TextType.CODE)

    def test_non_text_node(self):
        nodes = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("world", TextType.BOLD),
            TextNode(" `code`", TextType.TEXT)
        ]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("world", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode("", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_bold_delimiter(self):
        nodes = [TextNode("Hello **bold** text", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_italic_delimiter(self):
        nodes = [TextNode("Hello *italic* text", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        expected = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_mixed_delimiters(self):
        # This tests that the function handles one type of delimiter at a time
        nodes = [TextNode("Hello *italic* and **bold** text", TextType.TEXT)]
        result1 = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        expected1 = [
            TextNode("Hello *italic* and ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(result1, expected1)

if __name__ == "__main__":
    unittest.main()