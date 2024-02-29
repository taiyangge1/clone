import docx
from difflib import unified_diff


def read_docx(file_path):
    """读取Word文档的文本内容"""
    doc = docx.Document(file_path)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)


def compare_documents(doc1_path, doc2_path):
    """比较两个文档的内容并打印差异"""
    doc1_text = read_docx(doc1_path)
    doc2_text = read_docx(doc2_path)

    # 生成差异
    diff = unified_diff(
        doc1_text.splitlines(keepends=True),
        doc2_text.splitlines(keepends=True),
        fromfile='doc1',
        tofile='doc2',
    )

    # 打印差异
    print('\n'.join(diff))


# 调用函数比较两个文档
compare_documents(
    r"C:\Users\24766\Documents\WeChat Files\wxid_1plktyes67n822\FileStorage\File\2024-02\老.docx",
    r"C:\Users\24766\Documents\WeChat Files\wxid_1plktyes67n822\FileStorage\File\2024-02\新.docx"
)
