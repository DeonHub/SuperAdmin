// // // window.onload = function() {
// // //         let things = document.getElementsByTagName("input")
// // //         const inputs = Array.from(things)
// // //         inputs.forEach(input => {
// // //                 input.addEventListener('keypress', () => {
// // //                        if(input.readOnly == true){
// // //                                alert("This is a readonly field")
// // //                        }
// // //                 })
// // //         })
// // //       };

// // alert("Hello") 


// // alert("Hello") 

const upFile = (event) => {
        const attach_audio = document.getElementById('attach_audio')
        const web_class = document.getElementById('web_class')
        const audio_class = document.getElementById('audio_class')


        if(event.value == "web"){
                web_class.style.display = "block"
                audio_class.style.display = "none"
        }else if(event.value == "audio"){
                web_class.style.display = "none"
                audio_class.style.display = null
        }

}





function getData(){

        var requestOptions = {
                method: 'GET',
                redirect: 'follow'
              };

        var api_key='66d4824684db8ea0ab67fa76'
        var amount = document.getElementById('unit_amount_usd').value

        var response = fetch(`https://v6.exchangerate-api.com/v6/${api_key}/pair/USD/GHS/${amount}`, requestOptions)
                .then(response => response.json())
                .then(
                        result => {
                                // var url = result.conversion_result
                                document.getElementById('unit_amount_ghs').value = result.conversion_result
                        }
                )
                .catch(error => console.log('error', error));

}



// function getSize(){

//         var myHeaders = new Headers();
//         myHeaders.append("Content-Type", "application/json");
//         myHeaders.append("Cookie", "csrftoken=i0QCkPPQCUAYcsvB4MvYAfzl4HrLL0GJ");
//         myHeaders.append("Access-Control-Allow-Origin", "*");
        
//         var client_id = document.getElementById('client_size').value

//         // alert(client_id)

//         var raw = JSON.stringify({
//           "client_id": client_id
//         });
        
//         var requestOptions = {
//           method: 'POST',
//           headers: myHeaders,
//           body: raw,
//           redirect: 'follow'
//         };
        
//         fetch("http://127.0.0.1:8000/api/client-size/", requestOptions)
//           .then(response => response.json())
//           .then(
//                 result => {
//                         console.log(result)
//                         // document.getElementById('modula').value = result.info.membership_size
//                 }
//                 )
//           .catch(error => console.log('error', error));

// }





function addRen(){

        var inputCity1 = document.getElementById('inputCity1')
        var inputCity2 = document.getElementById('inputCity2')
        var inputZip = document.getElementById('inputZip')

        var special_unit_amount_usd = document.getElementById('special_unit_amount_usd')
        var special_unit_amount_ghs = document.getElementById('special_unit_amount_ghs')

        var unit_amount_usd = document.getElementById('unit_amount_usd')
        var unit_amount_ghs = document.getElementById('unit_amount_ghs')
        
        
        var duration = document.getElementById('sub_duration')


        var modula = document.getElementById('modula').value
        var paymentForm = document.getElementById('paymentForm')


        var url = paymentForm.getAttribute("data-modula-url")

        
        // alert("Inside")

        if(duration.value == ""){
            inputCity1.value = 0 * 30
            inputZip.value = 0 - parseInt(inputCity2.value)
            special_unit_amount_usd.value = 0
            special_unit_amount_ghs.value = 0
        }

        else{
                inputCity1.value = parseInt(duration.value) * 30
                inputZip.value = parseInt(inputCity1.value) - parseInt(inputCity2.value)
                special_unit_amount_usd.value = parseInt(duration.value) * parseInt(unit_amount_usd.value)
                special_unit_amount_ghs.value = parseInt(duration.value) * parseInt(unit_amount_ghs.value)
        }
        
}  





function changesValue(){

        var inputCity1 = document.getElementById('inputCity1')
        var inputCity2 = document.getElementById('inputCity2')
        var inputZip = document.getElementById('inputZip')

        var special_unit_amount_usd = document.getElementById('special_unit_amount_usd')
        var special_unit_amount_ghs = document.getElementById('special_unit_amount_ghs')

        var unit_amount_usd = document.getElementById('unit_amount_usd')
        var unit_amount_ghs = document.getElementById('unit_amount_ghs')
        
        
        var duration = document.getElementById('set_duration')


        var modula = document.getElementById('modula').value
        var paymentForm = document.getElementById('paymentForm')


        var url = paymentForm.getAttribute("data-modula-url")

        
        // alert("Inside")

        if(duration.value == ""){
            inputCity1.value = 0 * 30
            inputZip.value = 0 - parseInt(inputCity2.value)
            special_unit_amount_usd.value = 0
            special_unit_amount_ghs.value = 0
        }

        else{
                inputCity1.value = parseInt(duration.value)
                inputZip.value = parseInt(inputCity1.value) - parseInt(inputCity2.value)
                special_unit_amount_usd.value = parseInt(duration.value) * parseInt(unit_amount_usd.value)
                special_unit_amount_ghs.value = parseInt(duration.value) * parseInt(unit_amount_ghs.value)
        }
        
}  








function changedValue(){

        var inputCity1 = document.getElementById('inputCity1')
        var inputCity2 = document.getElementById('inputCity2')
        var inputZip = document.getElementById('inputZip')

        var special_unit_amount_usd = document.getElementById('special_unit_amount_usd')
        var special_unit_amount_ghs = document.getElementById('special_unit_amount_ghs')

        var unit_amount_usd = document.getElementById('unit_amount_usd')
        var unit_amount_ghs = document.getElementById('unit_amount_ghs')
        
        
        var duration = document.getElementById('set_duration')


        var modula = document.getElementById('modula').value
        var paymentForm = document.getElementById('paymentForm')


        var url = paymentForm.getAttribute("data-modula-url")

        var per_day_usd = parseInt(unit_amount_usd.value) / 30
        var per_day_ghs = parseInt(unit_amount_ghs.value) / 30

        // alert(per_day_usd)
        // alert(per_day_ghs)

        // alert("Inside")

        if(duration.value == ""){
            inputCity1.value = 0 * 30
            inputZip.value = 0 - parseInt(inputCity2.value)
            special_unit_amount_usd.value = 0
            special_unit_amount_ghs.value = 0
        }

        else{
                inputCity1.value = parseInt(duration.value)
                inputZip.value = parseInt(inputCity1.value) - parseInt(inputCity2.value)


                special_unit_amount_usd.value = Math.round(parseInt(duration.value) * parseFloat(per_day_usd))
                special_unit_amount_ghs.value = Math.round(parseInt(duration.value) * parseFloat(per_day_ghs))
        }
        
}  





const downFile = (event) => {
        const attach_audio = document.getElementById('attach_audio')
        const web_class = document.getElementById('web_class')
        const audio_class = document.getElementById('audio_class')


        if(event.value == "web"){
                web_class.style.display = "block"
                audio_class.style.display = "none"
        }else if(event.value == "audio"){
                web_class.style.display = "none"
                audio_class.style.display = null
        }

}


const checkOut = (event) => {
        const expire = document.getElementById('expire')

        if(event.checked == false){
                expire.style.display = "block"
        }
        else{
                expire.style.display = "none"
        }
        
}

const changeValue = () => {
        const duration = document.getElementById('set_duration')
        const unit_amount_usd = document.getElementById('unit_amount_usd')
        const unit_amount_ghs = document.getElementById('unit_amount_ghs')
        const total_amount_usd = document.getElementById('total_amount_usd')
        const total_amount_ghs = document.getElementById('total_amount_ghs')

        total_amount_usd.value = parseInt(duration.value) * parseInt(unit_amount_usd.value)
        total_amount_ghs.value = parseInt(duration.value) * parseInt(unit_amount_ghs.value)

}



const addValue = () => {
        const promo_discount = document.getElementById('promo_discount')
        const total_amount_usd = document.getElementById('special_unit_amount_usd')
        const total_amount_ghs = document.getElementById('special_unit_amount_ghs')
        const amount_usd = document.getElementById('amount_usd')
        const amount_ghs = document.getElementById('amount_ghs')

        // promo_discount
        // amount_usd
        // amount_ghs

        amount_usd.value = parseInt(total_amount_usd.value) - ((parseInt(promo_discount.value) * 0.01) * parseInt(total_amount_usd.value))
        amount_ghs.value = parseInt(total_amount_ghs.value) - ((parseInt(promo_discount.value) * 0.01) * parseInt(total_amount_ghs.value))
        // amount_ghs.value = parseInt(duration.value) * parseInt(unit_amount_ghs.value)

}


const getLogo = () => {

        const logo = document.getElementById('logo')
        const logoPreview = document.getElementById('logo-preview')
        const previewImage = document.querySelector(".logo-image")
        const previewTextDefault = document.querySelector(".logo-text")

        logo.addEventListener('change', function() {
                const file = this.files[0];
                
                if (file){

                        const reader = new FileReader()

                        previewTextDefault.style.display = "none"
                        previewImage.style.display = "block"
                        logoPreview.style.border = "none"

                        reader.addEventListener('load', function() {
                                console.log(this.result)
                                previewImage.setAttribute("src", this.result)  
                        });

                        reader.readAsDataURL(file);

                }else{
                        previewTextDefault.style.display = null
                        previewImage.style.display = null   
                        logoPreview.style.border = null
                        previewImage.setAttribute("src", "") 
                }
        })
}





function showDur(){
        dur = document.getElementById('dur')
        subscription_type = document.getElementById('subscription_type')

        
        if(subscription_type.value == "Account Activation"){
                dur.style.display= 'block';
        }
        else if(subscription_type.value == "Module Subscription"){
                dur.style.display= 'none';

        }
        else{
                dur.style.display= 'none';
        }
}


function pullDisc(source){
        disc = document.getElementById('disc')

        if (source.checked == true){
                disc.style.display = 'block';
        }
        else{
                disc.style.display = 'none';
        }
}


function toggle(source) {
        checkboxes = document.getElementsByName('foo[]');
        inputs = document.getElementsByName('foo[]');

        for(var i=0, n=checkboxes.length;i<n;i++) {
          checkboxes[i].checked = source.checked;

        //   document.getElementById("module"+i).disabled = false; 

        }
      }






const softCheck = () => {
        for(let i=1; i<100; i++){
                // let radio = document.getElementById("subject"+i)
                // let period = document.getElementById("module"+i)

                if(document.getElementById("subject"+i).checked){
                        document.getElementById("module"+i).disabled = false 

                }
                else{
                        document.getElementById("module"+i).disabled = true 
                }
                }
} 




const checkAmount = (event) => {
        var checked_values = []

        var selected_value = [];

        var sources = document.getElementsByClassName("source");

        Array.prototype.forEach.call(sources, function(e){
                if(e.checked){
                        selected_value.push(e.getAttribute("data-id"))
                        document.getElementById("duration"+e.getAttribute("data-id")).disabled = false;
                }else{
                        document.getElementById("duration"+e.getAttribute("data-id")).disabled = true;
                }
        });
}



const changeDur = (event) => {

        var day = document.getElementById("day");
        var month = document.getElementById("month");
        // var dur_type = document.getElementsById("dur_type");
        
        // alert(event.value)
        
        if(event.value == "days"){
                day.style.display = null;
                month.style.display = 'none';
        }else{
                day.style.display = 'none';
                month.style.display = null;     
        }
}




const memberOut = () => {
        // alert("Hello")
        window.localStorage.removeItem('token');
    }
    


function togglePassword() {

        var x = document.getElementById("password");

        if (x.type === "password") {
          x.type = "text";
        } else {
          x.type = "password";
        }

      }



      

// const changeDays = () => {

//         var selected_value = [];
//         var sources = document.getElementsByClassName("source");

//         Array.prototype.forEach.call(sources, function(e){
//                 let duration = document.getElementById("duration"+e.getAttribute("data-id"))
//                 let renewing_days = document.getElementById("renewing_days"+e.getAttribute("data-id"))
//                 let expired_days = document.getElementById("expired_days"+e.getAttribute("data-id"))
//                 let remaining_days = document.getElementById("remaining_days"+e.getAttribute("data-id"))
                
//                 if(e.checked){
//                         selected_value.push(e.getAttribute("data-id"))
//                 }else{
//                         selected_value.pop(e.getAttribute("data-id"))
//                 }

//                 if(duration.value == ""){
//                         renewing_days.value = 0 * 30
//                         if (expired_days.value == ""){
//                                 remaining_days.value = 0
//                             }
//                             else{
//                                 remaining_days.value = 0 - parseInt(expired_days.value)
//                             }
//                     }
            
//                 else{
//                         renewing_days.value = parseInt(duration.value) * 30

//                         if (expired_days.value == ""){
//                                 remaining_days.value = renewing_days.value
//                             }
//                             else{
//                                 remaining_days.value = parseInt(renewing_days.value) - parseInt(expired_days.value)

//                             }

//                 }


                
        
//         });

        
//         // var url = event.getAttribute("data-url");
//         // var modules = event.getAttribute("data-module");
//         // var modula = document.getElementById("modula").value;

//         return selected_value
// } 



const done = () => {
        data = {
                "School":"some"
        }
        return data

        //alert("Hello")
}





// $("#profiles-thread").select2({
//     minimumInputLength: 2,
//     tags: [],
//     ajax: {
//         url: URL,
//         dataType: 'json',
//         type: "GET",
//         quietMillis: 50,
//         data: function (term) {
//             return {
//                 term: term
//             };
//         },
//         results: function (data) {
//             return {
//                 results: $.map(data, function (item) {
//                     return {
//                         text: item.completeName,
//                         slug: item.slug,
//                         id: item.id
//                     }
//                 })
//             };
//         }
//     }
// });