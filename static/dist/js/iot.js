 $('.delete-company').click(function(){
 var id=$(this).attr("data-id");
 var check = confirm("Are you sure to delete the company?");
 if(check == true){
  $("#divLoading").show();
 $.ajax({
           url: "delete-company",
           type:"POST",
           data: {
              'id':id,'csrfmiddlewaretoken': token,
           },
           success: function(response) {
            $("#divLoading").hide();
           
               if(response.status){
                  alert('Company deleted successfully.');
                  window.location.reload();
               }
           }
       });
}
else{

    console.log("Company Request has be Cenceled.")
 }
});

 $('.delete-user').click(function(){
 var user=$(this).attr("data-id");
 var check_user = confirm("Are you sure to delete the user?");
 if(check_user == true){
    $("#divLoading").show();
   $.ajax({
           url: "delete-user",
           type:"POST",
           data: {
              'user':user,'csrfmiddlewaretoken': token,
           },
           success: function(response) {
                $("#divLoading").hide();
               if(response.status){
                  window.location.reload();
               }
               alert('User deleted successfully.');
           }
       });
 }
 else{

    console.log("Request has be Cenceled.")
 }

});



$('.delete-zone').click(function(){
 var id=$(this).attr("data-id");
 var check_user = confirm("Are you sure to delete the zone?");
 if(check_user == true){
    $("#divLoading").show();
   $.ajax({
           url: "delete-zone",
           type:"POST",
           data: {
              'id':id,'csrfmiddlewaretoken': token,
           },
           success: function(response) {
              
               if(response.status){
                  window.location.reload();
                  $("#divLoading").hide();
                  alert('Zone deleted successfully.');
               }
                
           }
       });
 }
 else{

    console.log("Request has been Canceled.")
 }

});


$('.delete-sensor-type').click(function(){
 var id=$(this).attr("data-id");
 var check_user = confirm("Are you sure to delete the sensor type?");
 if(check_user == true){
  $("#divLoading").show();
   $.ajax({
           url: "delete-sensor-type",
           type:"POST",
           data: {
              'id':id,'csrfmiddlewaretoken': token,
           },
           success: function(response) {
            
               if(response.status){
                  window.location.reload();
               }
               $("#divLoading").show();
                alert('Sensortype deleted successfully.');
           }
       });
 }
 else{

    console.log("Request has been Canceled.")
 }

});


$('.delete-sensor').click(function(){
 var id=$(this).attr("data-id");
 var check_user = confirm("Are you sure to delete the sensor?");
 if(check_user == true){
   $.ajax({
           url: "delete-sensor",
           type:"POST",
           data: {
              'id':id,'csrfmiddlewaretoken': token,
           },
           success: function(response) {
            
               if(response.status){
                  window.location.reload();
               }
                alert('Sensor deleted successfully.');
           }
       });
 }
 else{

    console.log("Request has been Canceled.")
 }

});

$('.delete-workflow').click(function(){
 var id=$(this).attr("data-id");
 var check_user = confirm("Are you sure to delete the workflow?");
 if(check_user == true){
   $.ajax({
           url: "delete-workflow",
           type:"POST",
           data: {
              'id':id,'csrfmiddlewaretoken': token,
           },
           success: function(response) {
            
               if(response.status){
                  window.location.reload();
               }
                alert('Workflow deleted successfully.');
           }
       });
 }
 else{

    console.log("Request has been Canceled.")
 }

});


$('.delete-object-sensor-mapping').click(function(){
 var id=$(this).attr("data-id");
 var check_user = confirm("Are you sure to delete the object sensor mapping?");
 if(check_user == true){
   $.ajax({
           url: "delete-object-sensor-mapping",
           type:"POST",
           data: {
              'id':id,'csrfmiddlewaretoken': token,
           },
           success: function(response) {
            
               if(response.status){
                  window.location.reload();
               }
                alert('Object sensor mapping deleted successfully.');
           }
       });
 }
 else{

    console.log("Request has been Canceled.")
 }

});