function clickMe() {
    var tag=document.getElementById("content");
    var userInputData=tag.value;
    var tagText=document.getElementById("txt");
    tagText.innerText=userInputData;
}