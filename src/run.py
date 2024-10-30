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
    print("extensions:",extensions)
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

    templatePaths = gr.State([
        os.path.join("./res", f)
        for f in os.listdir("./res")
        if (os.path.isfile(os.path.join("./res", f)) and f.endswith(".docx"))
    ])
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
    def updateTemplatePath(t):

        templatePaths.value = [
            os.path.join("./res", f)
            for f in os.listdir("./res")
            if (os.path.isfile(os.path.join("./res", f)) and f.endswith(".docx"))
        ]
        print("onLoad ")
        print(templatePaths.value)
        t.choices = templatePaths.value
        return gr.Radio(
            label="模板路径",
            info="用于调整模板路径,位于./res/下,默认为./res/template.docx",
            value="./res/template.docx",
            choices=templatePaths.value,
        )

    with gr.Blocks() as demo:
        title = "收集源代码生成文档"
        description = "This is a demo for Docx Handler"
        with gr.Row(equal_height=True):
            name = gr.Textbox(
                label="项目名",
                info="项目名,用于生成标题和页眉",
                placeholder="输入项目名",
                scale=3
            )
            pageSize = gr.Number(
                label="总页数",
                value=60,
                info="若真实页数过多则截取首尾各1/2总页数",
                scale=2
            )
            headerFontSize = gr.Number(
                label="大标题字号", info="用于调整标题字体大小", value=26,scale=1
            )
            heading1FontSize = gr.Number(
                label="小标题字号", info="用于调整文件名字体大小", value=12,scale=1
            )
        with gr.Row():
            enFontName = gr.Textbox(
                label="英文字体",
                info="用于调整英文字体,需为系统已安装的字体，如：Times New Roman",
                value="Times New Roman",
            )
            zhFontName = gr.Textbox(
                label="中文字体",
                info="用于调整中文字体,需为系统已安装的字体，如：宋体",
                value="宋体",
            )
        with gr.Row(equal_height=True):
            titleSuffix = gr.Textbox(
                label="标题后缀",
                info="用于调整标题后缀,，如：程序鉴别文档，合成的标题为：项目名-后缀",
                value="程序鉴别材料",
            )
            templatePath = gr.Radio(
                label="模板路径",
                info="用于调整模板路径,位于./res/下,默认为./res/template.docx",
                value="./res/template.docx",
                choices=templatePaths.value
            )
            demo.load(fn=lambda: updateTemplatePath(templatePath),outputs=templatePath)

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
                item=gr.Textbox(label=f"扩展名-{i+1}", value=val,info="目标源代码文件后缀，如：java，注意无需加点")
                item.change(onChangeExtension,inputs=[extensionsState,gr.State(i), item],outputs=extensionsState)
                extensionsBoxs.append(item)
            return extensions
        addButton.click(addExtension,inputs=extensionsState,outputs=extensionsState)
        removeButton.click(removeExtension,inputs=extensionsState,outputs=extensionsState,)

        directory=gr.Textbox(label="源代码目录",info="目标源代码文件所在目录，如：/Users/a/Code/Java/")
        processButton=gr.Button("开始处理")

        render_boxes = gr.Group(
            name,
            pageSize,
            headerFontSize,
            heading1FontSize,
            enFontName,
            zhFontName,
            titleSuffix,
            templatePath,
            extensionsBoxs,
            addButton,
            removeButton,
            directory,
            processButton,
        )

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
