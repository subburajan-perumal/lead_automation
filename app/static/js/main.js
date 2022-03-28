function test(){
    console.log("test working")
}


function changeText(el) {
  document.getElementById('myTextArea').value = el.value;
}


function validationEvent(){
  site_name=document.getElementsByName('site_name');
  result=validURL("tesiting.com")
  console.log(result)
  if (result==true)
  {
    return false;
  }
  console.log(result)
  return false
}

function change_data(){

}

function validURL(str) {
    var pattern = new RegExp('^(https?:\\/\\/)?'+ // protocol
      '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|'+ // domain name
      '((\\d{1,3}\\.){3}\\d{1,3}))'+ // OR ip (v4) address
      '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*'+ // port and path
      '(\\?[;&a-z\\d%_.~+=-]*)?'+ // query string
      '(\\#[-a-z\\d_]*)?$','i'); // fragment locator
    return !!pattern.test(str);
  }

function IsJsonString(str) {
    try {
        JSON.parse(str);
    } catch (e) {
        return false;
    }
    return true;
}