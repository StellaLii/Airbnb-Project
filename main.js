// animation function for scrolling down the page
const navLinks = document.querySelectorAll("nav ul li a");
// console.log(navLinks)
for (const link of navLinks) {
  link.addEventListener("click", clickHandler);
}
function clickHandler(e) {
  e.preventDefault();
  const href = this.getAttribute("href");
  const offsetTop = document.querySelector(href).offsetTop;

  scroll({
    top: offsetTop,
    behavior: "smooth"
  });
}



$('#submit').click(function(){ 
  // fetching form data
  var formData = {
        Address: document.getElementById("address").value,
        Num_Bedroom: document.getElementById("bedrooms").value,
        Num_Bathroom: document.getElementById("bathrooms").value,
        Refrigerator: $("#Refrigerator").is(':checked'),
        Stove: $("#Stove").is(':checked'),
        Microwave: $("#Microwave").is(':checked'),
        Dishwasher: $("#Dishwasher").is(':checked'),
        Heating: $("#Heating").is(':checked'),
        AC: $("#AC").is(':checked'),
        Air_Conditioning: $("#Air-Conditioning").is(':checked'),
        Parking: $("#Parking").is(':checked'),
        Network: $("#Network").is(':checked'),
        Hair_dryer: $("#Hair-dryer").is(':checked'),
        Washer: $("#Washer").is(':checked'),
        Dryer: $("#Dryer").is(':checked'),
        TV: $("#TV").is(':checked'),
  }

  $.ajax({ 
       // method
       type: "POST",
       // content-type
       contentType: "application/json",
       // payload
       data: JSON.stringify(formData),
       // endpoint url
       url: "change to your api link",
       // on success
       success: function(data){        
          console.log("Success", data);
          const status = document.getElementById("status-text");
          status.textContent = data["body"];
          const result_text = document.getElementById("result-text");
          result_text.textContent = data["result"];
         
       },
       // on error
       error: function(data){        
          console.log("Error", data);
       }
   });
});