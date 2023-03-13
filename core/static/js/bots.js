var script = document.createElement('script')
script.src = 'https://code.jquery.com/jquery-3.6.3.min.js'
document.getElementsByTagName('head')[0].appendChild(script)

var myForm = document.getElementById('pair_input_form');
myForm.addEventListener('submit',key_validator);


function key_validator(event) {

    var allInputs = myForm.getElementsByTagName('input');
    const data = new URLSearchParams();
    let proper_len = {
        "secret" : true,
        "public" : true
    };
    for (var i = 0; i < allInputs.length; i++) {
        let input = allInputs[i];
        if (input.name && !input.value) {
            event.preventDefault();
            alert("Please fill all the fields!");
            return false;
        }
        data.append(input.name,input.value);
    }
    
    if(allInputs[2].name == 'secret_key'  && allInputs[2].value.length != 64){
        proper_len['secret'] = false
    }
    if(allInputs[1].name == 'public_key'  && allInputs[1].value.length != 64){
        proper_len['public'] = false
    }
    if(proper_len['secret'] == false && proper_len['public'] == false){
        alert("Both keys should be 64 characters long!")
    }
    else if(proper_len['secret'] == false){
        alert("Secret key should be 64 characters long!")
    }
    else if(proper_len['public'] == false){
        alert("Public key be 64 characters long!")
    }
    else{
        fetch(window.location.href,{
            method: 'POST',
            body: data
        })
    }
    if(proper_len['secret'] == false || proper_len['public'] == false){
        event.preventDefault();
    }
}

