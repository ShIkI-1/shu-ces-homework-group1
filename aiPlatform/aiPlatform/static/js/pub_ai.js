window.onload = function () {
    const {createEditor, createToolbar} = window.wangEditor

    const editorConfig = {
        placeholder: 'Type here...',
        onChange(editor) {
            const html = editor.getHtml()
            console.log('editor content', html)
            // 也可以同步到 <textarea>
        }
    }

    const editor = createEditor({
        selector: '#editor-container',
        html: '<p><br></p>',
        config: editorConfig,
        mode: 'default', // or 'simple'
    })

    const toolbarConfig = {}

    const toolbar = createToolbar({
        editor,
        selector: '#toolbar-container',
        config: toolbarConfig,
        mode: 'default', // or 'simple'
    })

    $("#pub").click(function (event) {
    event.preventDefault();
    let title = $("input[name='title']").val();
    let intro = $("input[name='intro']").val();
    let flexibility = $("input[name='flexibility']").val();
    let randomness = $("input[name='randomness']").val();
    let price = $("input[name='price']").val();
    let text = editor.getHtml();
    $.ajax('/prompt/pub', {
        method: 'POST',
        data: { title, intro, flexibility, randomness, price, text },
        success: function(response) {
            console.log("Success:", response);
            // 跳转到 /prompt 页面
            window.location.href = '/prompt';
        },
        error: function(xhr) {
            console.log("Error:", xhr.responseText);
        }
    });
});

}