from docx_handler import DocxHandler
import gradio as gr

def initAndProcess(name=None,
        pageSize=None,
        HeaderFontSize=None,
        Heading1FontSize=None,
        enFontName=None,
        zhFontName=None,
        titleSuffix=None,
        templatePath=None,
        extensions=None,
        directory=None,):
    dh = DocxHandler(
        name=name,
        pageSize=pageSize,
        HeaderFontSize=HeaderFontSize,
        Heading1FontSize=Heading1FontSize,
        enFontName=enFontName,
        zhFontName=zhFontName,
        titleSuffix=titleSuffix,
        templatePath=templatePath,
        extensions=extensions,
        directory=directory,
    )
    return dh.process()

if __name__ == "__main__":
    # dh = DocxHandler(
    #     name="test",
    #     directory="/Users/yushaochen/Code/Java/lims/",
    # )

    # dh = DocxHandler()
    # dh.process()
    codeSufixs=gr.Blocks()
    with codeSufixs:
        newItem=gr.components.Textbox(label="源代码后缀")
        addButton = gr.components.Button("添加")
        itemListDisplay = gr.components.Textbox(label="源代码后缀列表")
        itemListState=gr.State(value=[])
        addButton.click(
            fn=lambda newItem,itemList:itemList.append(newItem.value),
            inputs=[newItem,itemListState],
            outputs=None,
            after_update=lambda newItem,itemList:itemListDisplay.update("\n".join(itemList))
        )
        itemListDisplay.update("\n".join(itemListState.value))

    demo = gr.Interface(
        fn=initAndProcess,
        inputs=[
            gr.components.Textbox(label="项目名", info="项目名,用于生成标题和页眉"),
            gr.components.Number(
                label="总页数",
                value=60,
                info="总页数，若真实页数多于该页数，截取首尾各1/2总页数的页面",
            ),
            gr.components.Number(label="大标题字号", info="用于调整标题字体大小"),
            gr.components.Number(label="小标题字号", info="用于调整文件名字体大小"),
            gr.components.Textbox(
                label="英文字体",
                info="用于调整英文字体,需为系统已安装的字体，如：Times New Roman",
            ),
            gr.components.Textbox(
                label="中文字体", info="用于调整中文字体,需为系统已安装的字体，如：宋体"
            ),
            gr.components.Textbox(
                label="标题后缀",
                info="用于调整标题后缀,，如：程序鉴别文档，合成的标题为：项目名-后缀",
            ),
            gr.components.Textbox(
                label="模板路径", info="用于调整模板路径,默认为./res/template.docx"
            ),
            codeSufixs,
            gr.components.Textbox(label="源代码目录"),
        ],
        outputs=gr.components.File(label="输出文件"),
        title="收集源代码生成文档",
        description="This is a demo for Docx Handler",
    )
    demo.launch()
