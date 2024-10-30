from docx_handler import DocxHandler
import gradio as gr
import os


def initAndProcess(
    name=None,
    pageSize=None,
    HeaderFontSize=None,
    Heading1FontSize=None,
    enFontName=None,
    zhFontName=None,
    titleSuffix=None,
    templatePath=None,
    extensions=None,
    directory=None,
):
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

    # 获取./res/下所有文件作为模版列表

    templatePaths = [
        os.path.join("./res", f)
        for f in os.listdir("./res")
        if (os.path.isfile(os.path.join("./res", f)) and f.endswith(".docx"))
    ]
    print(templatePaths)

    def addExtension(inputs):
        inputs.append("")
        return inputs

    def removeExtension(inputs):
        if len(inputs)>1:
            inputs.pop()
        return inputs
    def onChangeExtension(inputs,index,value):
        inputs[index]=value
        return inputs

    with gr.Blocks() as demo:
        title = "收集源代码生成文档"
        description = "This is a demo for Docx Handler"

        name=gr.Textbox(label="项目名", info="项目名,用于生成标题和页眉",placeholder="输入项目名")
        pageSize= gr.Number(
            label="总页数",
            value=60,
            info="总页数，若真实页数多于该页数，截取首尾各1/2总页数的页面",
        )
        headerFontSize=gr.Number(
            label="大标题字号", info="用于调整标题字体大小", value=26
        )
        heading1FontSize=gr.Number(
            label="小标题字号", info="用于调整文件名字体大小", value=12
        )
        enFontName=gr.Textbox(
            label="英文字体",
            info="用于调整英文字体,需为系统已安装的字体，如：Times New Roman",
            value="Times New Roman",
        )
        zhFontName=gr.Textbox(
            label="中文字体",
            info="用于调整中文字体,需为系统已安装的字体，如：宋体",
            value="宋体",
        )
        titleSuffix=gr.Textbox(
            label="标题后缀",
            info="用于调整标题后缀,，如：程序鉴别文档，合成的标题为：项目名-后缀",
            value="程序鉴别材料",
        )
        templatePath=gr.Radio(
            label="模板路径",
            info="用于调整模板路径,位于./res/下,默认为./res/template.docx",
            value="./res/template.docx",
            choices=templatePaths,
        )
        # extensions=gr.Textbox(
        #     label="源代码后缀", info="目标源代码文件后缀，如：.java"
        # )

        extensionsState = gr.State([""])
        extensionsBoxs=[]
        with gr.Row():
            addButton = gr.Button("添加扩展名")
            removeButton = gr.Button("移除扩展名")
        @gr.render(inputs=extensionsState,triggers=[addButton.click,removeButton.click,demo.load])
        def updateExtensions(extensions):
            print([box for box in extensions])
            extensionsBoxs.clear()
            for i,val in enumerate(extensions):
                item=gr.Textbox(label=f"扩展名{i+1}", value=val)
                item.change(onChangeExtension,inputs=[extensionsState,gr.State(i), item],outputs=extensionsState)
                extensionsBoxs.append(item)
            return extensions
        addButton.click(addExtension,inputs=extensionsState,outputs=extensionsState)
        removeButton.click(removeExtension,inputs=extensionsState,outputs=extensionsState,)
        render_boxes = gr.Group(extensionsBoxs)
        directory=gr.Textbox(label="源代码目录")
        processButton=gr.Button("开始处理")
        outputs = gr.File(
            label="输出文件",
        )

        # main=gr.Group([name, pageSize, headerFontSize, heading1FontSize, enFontName, zhFontName, titleSuffix, templatePath, extensions, directory, render_boxes,extensionsBoxs, processButton])
        processButton.click(
            fn=initAndProcess,
            inputs=[
                name,
                pageSize,
                headerFontSize,
                heading1FontSize,
                enFontName,
                zhFontName,
                titleSuffix,
                templatePath,
                extensionsState,
                directory,
            ],
            outputs=outputs,
        )

    demo.launch()
