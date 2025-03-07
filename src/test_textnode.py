import unittest

from textnode import (
    TextNode, 
    TextType,
    BlockType, 
    split_nodes_delimiter, 
    extract_markdown_links, 
    extract_markdown_images,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    markdown_to_blocks,
    block_to_block_type
    )

from htmlnode import text_node_to_html_node


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
            TextNode("more code", TextType.CODE)
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
            TextNode("code", TextType.CODE)
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

    def test_split_nodes_image_basic(self):
        nodes = [TextNode("Hello ![image](url) world", TextType.TEXT)]
        result = split_nodes_image(nodes)
        expected = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "url"),
            TextNode(" world", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_image_no_images(self):
        nodes = [TextNode("Hello world", TextType.TEXT)]
        result = split_nodes_image(nodes)
        expected = [TextNode("Hello world", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_split_nodes_image_multiple(self):
        nodes = [TextNode("![first](url1) between ![second](url2)", TextType.TEXT)]
        result = split_nodes_image(nodes)
        expected = [
            TextNode("first", TextType.IMAGE, "url1"),
            TextNode(" between ", TextType.TEXT),
            TextNode("second", TextType.IMAGE, "url2"),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_image_at_start(self):
        nodes = [TextNode("![image](url) rest of text", TextType.TEXT)]
        result = split_nodes_image(nodes)
        expected = [
            TextNode("image", TextType.IMAGE, "url"),
            TextNode(" rest of text", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_image_at_end(self):
        nodes = [TextNode("beginning ![image](url)", TextType.TEXT)]
        result = split_nodes_image(nodes)
        expected = [
            TextNode("beginning ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "url"),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_adjacent_images(self):
        nodes = [TextNode("![one](url1)![two](url2)", TextType.TEXT)]
        result = split_nodes_image(nodes)
        expected = [
            TextNode("one", TextType.IMAGE, "url1"),
            TextNode("two", TextType.IMAGE, "url2"),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_image_complex_url(self):
        nodes = [TextNode("Start ![complex](https://example.com/image.jpg?size=large#fragment) end", TextType.TEXT)]
        result = split_nodes_image(nodes)
        expected = [
            TextNode("Start ", TextType.TEXT),
            TextNode("complex", TextType.IMAGE, "https://example.com/image.jpg?size=large#fragment"),
            TextNode(" end", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_image_with_spaces(self):
        nodes = [TextNode("![alt text with spaces](image url with spaces)", TextType.TEXT)]
        result = split_nodes_image(nodes)
        expected = [
            TextNode("alt text with spaces", TextType.IMAGE, "image url with spaces"),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_image_multiple_with_text(self):
        nodes = [TextNode("Start ![one](url1) middle ![two](url2) ![three](url3) end", TextType.TEXT)]
        result = split_nodes_image(nodes)
        expected = [
            TextNode("Start ", TextType.TEXT),
            TextNode("one", TextType.IMAGE, "url1"),
            TextNode(" middle ", TextType.TEXT),
            TextNode("two", TextType.IMAGE, "url2"),
            TextNode("three", TextType.IMAGE, "url3"),
            TextNode(" end", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_image_empty_alt_text(self):
        nodes = [TextNode("![](url)", TextType.TEXT)]
        result = split_nodes_image(nodes)
        expected = [
            TextNode("", TextType.IMAGE, "url"),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_link_basic(self):
        nodes = [TextNode("Click [here](url) now", TextType.TEXT)]
        result = split_nodes_link(nodes)
        expected = [
            TextNode("Click ", TextType.TEXT),
            TextNode("here", TextType.LINK, "url"),
            TextNode(" now", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_link_no_links(self):
        nodes = [TextNode("Plain text", TextType.TEXT)]
        result = split_nodes_link(nodes)
        expected = [TextNode("Plain text", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_split_nodes_link_no_links(self):
        nodes = [TextNode("Plain text", TextType.TEXT)]
        result = split_nodes_link(nodes)
        expected = [TextNode("Plain text", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_split_nodes_link_multiple(self):
        nodes = [TextNode("Start [link1](url1) middle [link2](url2) end", TextType.TEXT)]
        result = split_nodes_link(nodes)
        expected = [
            TextNode("Start ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "url1"),
            TextNode(" middle ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "url2"),
            TextNode(" end", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_link_at_start(self):
        nodes = [TextNode("[link](url) rest of text", TextType.TEXT)]
        result = split_nodes_link(nodes)
        expected = [
            TextNode("link", TextType.LINK, "url"),
            TextNode(" rest of text", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_link_at_end(self):
        nodes = [TextNode("beginning [link](url)", TextType.TEXT)]
        result = split_nodes_link(nodes)
        expected = [
            TextNode("beginning ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url"),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_adjacent_links(self):
        nodes = [TextNode("[one](url1)[two](url2)", TextType.TEXT)]
        result = split_nodes_link(nodes)
        expected = [
            TextNode("one", TextType.LINK, "url1"),
            TextNode("two", TextType.LINK, "url2"),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_link_complex_url(self):
        nodes = [TextNode("Check [this](https://example.com/path?param=1#fragment) out", TextType.TEXT)]
        result = split_nodes_link(nodes)
        expected = [
            TextNode("Check ", TextType.TEXT),
            TextNode("this", TextType.LINK, "https://example.com/path?param=1#fragment"),
            TextNode(" out", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_link_with_spaces(self):
        nodes = [TextNode("[link with spaces](url with spaces)", TextType.TEXT)]
        result = split_nodes_link(nodes)
        expected = [
            TextNode("link with spaces", TextType.LINK, "url with spaces"),
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_multiple_empty_texts(self):
        nodes = [TextNode("[one](url1) [two](url2) [three](url3)", TextType.TEXT)]
        result = split_nodes_link(nodes)
        expected = [
            TextNode("one", TextType.LINK, "url1"),
            TextNode("two", TextType.LINK, "url2"),
            TextNode("three", TextType.LINK, "url3"),
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnode(self):
        text = "Hello world"
        result = text_to_textnodes(text)
        expected = [TextNode("Hello world", TextType.TEXT)]
        self.assertEqual(result, expected)

    def test_text_to_textnode_bold(self):
        text = "Hello **world**"
        result = text_to_textnodes(text)
        expected = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("world", TextType.BOLD)
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnode_code(self):
        text = "Hello `code` world"
        result = text_to_textnodes(text)
        expected = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" world", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_text_to_textnode_image_link(self):
        text = "Click [here](https://boot.dev) and ![alt](image.jpg)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("Click ", TextType.TEXT),
            TextNode("here", TextType.LINK, "https://boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "image.jpg")
        ]
        self.assertEqual(result, expected)    

    def test_text_to_textnode_bold_middle(self):
        text = "Hello **bold** world"
        result = text_to_textnodes(text)
        expected = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" world", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_simple_heading_and_paragraph(self):
        md = """
    # Heading 1\n\nThis is a paragraph.
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading 1", 
                "This is a paragraph."
            ],
        )

    def test_markdown_to_blocks_mixed_blocks(self):
        md = """
    # A heading\n\n\nThis is a paragraph.\n\n- List item 1\n- List item 2\n\n
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# A heading", 
                "This is a paragraph.", 
                "- List item 1\n- List item 2"
            ],
        )

    def test_markdown_to_blocks_single_block(self):
        md = """
    > This is a blockquote.
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "> This is a blockquote."
            ],
        )    

    def test_markdown_to_blocks_empty(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [],
        ) 

    def test_markdown_to_blocks_multiple_newlines(self):
        md = """
    First block\n\n\n\nSecond block\n\n\nThird block
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First block", 
                "Second block", 
                "Third block"
            ],
        ) 

    def test_markdown_to_blocks_indented_block(self):
        md = """
        code block with\n    indents\n\nAnother block
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "code block with\nindents", 
                "Another block"
            ],
        )     

class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type_paragraph(self):
        block = """
        This is a simple paragraph.
        It can span multiple lines.
    """
        result = block_to_block_type(block)
        expected = BlockType.paragraph
        self.assertEqual(result, expected)

    def test_block_to_block_type_paragraph2(self):
        block = "Just a single line paragraph."
        result = block_to_block_type(block)
        expected = BlockType.paragraph
        self.assertEqual(result, expected)    

    def test_block_to_block_type_heading(self):
        block = "# Heading level 1"
        result = block_to_block_type(block)
        expected = BlockType.heading
        self.assertEqual(result, expected)     

    def test_block_to_block_type_heading2(self):
        block = "###### Heading level 6"
        result = block_to_block_type(block)
        expected = BlockType.heading
        self.assertEqual(result, expected)
        
    def test_block_to_block_type_invalid_heading(self):
        block = "####### Invalid heading"
        result = block_to_block_type(block)
        expected = BlockType.paragraph
        self.assertEqual(result, expected)

    def test_block_to_block_type_invalid_heading2(self):
        block = "#Invalid heading"
        result = block_to_block_type(block)
        expected = BlockType.paragraph
        self.assertEqual(result, expected)

    def test_block_to_block_type_code(self):
        block = """```
function example() {
return "Hello World";
}
```"""
        result = block_to_block_type(block)
        expected = BlockType.code
        self.assertEqual(result, expected)      

    def test_block_to_block_type_code2(self):
        block = """```
Single line code
```"""
        result = block_to_block_type(block)
        expected = BlockType.code
        self.assertEqual(result, expected)     

    def test_block_to_block_type_quote(self):
        block = """> This is a quote
> More quote text"""
        result = block_to_block_type(block)
        expected = BlockType.quote
        self.assertEqual(result, expected) 

    def test_block_to_block_type_quote2(self):
        block = "> Single line quote"
        result = block_to_block_type(block)
        expected = BlockType.quote
        self.assertEqual(result, expected)

    def test_block_to_block_type_invalid_quote(self):
        block = """> First line is quote
Second line is not"""
        result = block_to_block_type(block)
        expected = BlockType.paragraph
        self.assertEqual(result, expected)  

    def test_block_to_block_type_unordered_list(self):
        block = """- Item one
- Item two
- Item three"""
        result = block_to_block_type(block)
        expected = BlockType.unordered_list
        self.assertEqual(result, expected) 

    def test_block_to_block_type_unordered_list2(self):
        block = "- Single item list"
        result = block_to_block_type(block)
        expected = BlockType.unordered_list
        self.assertEqual(result, expected)

    def test_block_to_block_type_invalid_unordered_list(self):
        block = """- First item
Second item without dash"""
        result = block_to_block_type(block)
        expected = BlockType.paragraph
        self.assertEqual(result, expected)

    def test_block_to_block_type_ordered_list(self):
        block = """1. First item
2. Second item
3. Third item"""
        result = block_to_block_type(block)
        expected = BlockType.ordered_list
        self.assertEqual(result, expected)

    def test_block_to_block_type_ordered_list2(self):
        block = "1. Single item ordered list"
        result = block_to_block_type(block)
        expected = BlockType.ordered_list
        self.assertEqual(result, expected)

    def test_block_to_block_type_invalid_ordered_list(self):
        block = """1. First item
3. Third item"""
        result = block_to_block_type(block)
        expected = BlockType.paragraph
        self.assertEqual(result, expected)

    def test_block_to_block_type_invalid_ordered_list2(self):
        block = """1. First item
2. Second item
4. Fourth item"""
        result = block_to_block_type(block)
        expected = BlockType.paragraph
        self.assertEqual(result, expected)

    def test_block_to_block_type_invalid_ordered_list3(self):
        block = """2. Starts with 2 instead of 1
3. Continues with 3"""
        result = block_to_block_type(block)
        expected = BlockType.paragraph
        self.assertEqual(result, expected)

    def test_block_to_block_type_invalid_ordered_list4(self):
        block = """1. Item
2. Item
3. Item
 4. Indented item (not starting at beginning)"""
        result = block_to_block_type(block)
        expected = BlockType.paragraph
        self.assertEqual(result, expected)

    def test_block_to_block_type_edge_case(self):
        block = """1. This looks like an ordered list
But the second line doesn't follow the pattern"""
        result = block_to_block_type(block)
        expected = BlockType.paragraph
        self.assertEqual(result, expected)

    def test_block_to_block_type_edge_case2(self):
        block = """- This looks like an unordered list
> But the second line is a quote"""
        result = block_to_block_type(block)
        expected = BlockType.paragraph
        self.assertEqual(result, expected)

    def test_block_to_block_type_edge_case3(self):
        block = """```
This has code markers
```
But also has extra content after closing"""
        result = block_to_block_type(block)
        expected = BlockType.paragraph
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()