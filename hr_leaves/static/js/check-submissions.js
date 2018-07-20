var selected = [] ;
var old_rating_id ; 
var currentElement = 1 ;
function handleCheckBoxClick(id) {
    var elem = document.getElementById(id);
    if(elem != null && id != null) {
        if (elem.checked == true) {
          if (currentElement <= 3) {
              switch(currentElement){
                case 1: {
                    document.getElementById('id_agency1').value = id ;
                    break;
                }
                case 2: {
                    document.getElementById('id_agency2').value = id ;
                    break;
                }
                case 3: {
                    document.getElementById('id_agency3').value = id ;
                    break;
                }
            } 
            if (currentElement < 3) {
                currentElement += 1 ;
                }
          } else {
              elem.checked = false;
          }
        } else {
            switch(currentElement){
                case 1: {
                    document.getElementById('id_agency1').value = '' ;
                    break;
                }
                case 2: {
                    document.getElementById('id_agency2').value = '' ;
                    break;
                }
                case 3: {
                    document.getElementById('id_agency3').value = '' ;
                    break;
                }
            }
            if (currentElement > 1) {
                currentElement -= 1 ;
            }
       }
    }
}

function handleUserValidationClick(id){
    var elem = document.getElementById(id);
    if(elem != null) {
        if (elem.checked == true) {
        //var inputs = document.getElementsByTagName('input');
        jQuery.noConflict();
        $('#raison').modal();
          var inputs = document.querySelectorAll('input[type="checkbox"]');
            for(i = 0; i < inputs.length; i++) {
                if(inputs[i].id != id)
                   inputs[i].checked = false;
                 }
            document.getElementById('id_suggestion').value = id ;
        } else {
            document.getElementById('id_suggestion').value = "" ;
        }
    } else {
        console.log('unable to get html element with id'+id) ;
    }
}

function handleUserPaiementClick(id){
    var elem = document.getElementById(id);
    if(elem != null) {
        if (elem.checked == true) {
        jQuery.noConflict();
        $('#paiement-confirmation').modal();
          var inputs = document.querySelectorAll('input[type="checkbox"]');
            for(i = 0; i < inputs.length; i++) {
                if(inputs[i].id != id)
                   inputs[i].checked = false;
                 }
            document.getElementById('id_suggestion').value = id ;
        } else {
            document.getElementById('id_suggestion').value = "" ;
        }
    } else {
        console.log('unable to get html element with id'+id) ;
    }
}

function hideCheckboxModal(id){
    console.log('hide checkbox');
    $('#'+id).modal('hidden');
    var inputs = document.querySelectorAll('input[type="checkbox"]');
    for(i = 0; i < inputs.length; i++) {
        if(inputs[i].id != id)
           inputs[i].checked = false;
    }
    document.getElementById('id_suggestion').value = "" ;
}

function handleRatingClick(id){
    jQuery.noConflict();
    $('#rating').modal();
    document.getElementById('id_rating').value = id ;

    // if it's a new submission then we re-init the form
    if(old_rating_id != id) {
        $('#rating_score')[0].selectedIndex = 0;
        $('#id_rating_raison').val('');
    }
    
    old_rating_id = id;
}
