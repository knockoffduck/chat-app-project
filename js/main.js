$(document).ready(function () {
    $("#create").click(() => {
        const inputValue = $("#myInput").val();
        $("#randomList").append(`<p id="result">${inputValue}</p>`)

    })
})