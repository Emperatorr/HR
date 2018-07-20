function load_dep_place(country, city){
	for(let cpt=0; cpt<2; cpt++) {
		var i, p, valeur;
		$.getJSON('../../../static/json/pays.json', function(data){
			$('#id_form-'+cpt+'-departure_country').empty();
			$('#id_form-'+cpt+'-departure_city').empty();
			$('#id_form-'+cpt+'-departure_country').append("<option value=''>----------</option>");
			$('#id_form-'+cpt+'-departure_city').append("<option value=''>----------</option>");
			$.each(data, function(index, d){
				if (country == d.code) {
					$('#id_form-'+cpt+'-departure_country').append('<option selected value=\'' + d.code + '\'>' + d.pays + '</option>');
				} else{
					$('#id_form-'+cpt+'-departure_country').append('<option value=\'' + d.code + '\'>' + d.pays + '</option>');
				}
				valeur = $('#id_form-'+cpt+'-departure_country').val();
				$.each(data, function(index, d){
					if(valeur == d.pays){
						$('#id_form-'+cpt+'-departure_city').empty();
						for (i = 0; i < d.villes.length; i++) {
							if (city == d.villes[i]) {
							   $('#id_form-'+cpt+'-departure_city').append('<option selected value=\'' + d.villes[i] + '\'>' + d.villes[i] + '</option>');
							} else{
								$('#id_form-'+cpt+'-departure_city').append('<option value=\'' + d.villes[i] + '\'>' + d.villes[i] + '</option>');
							}
						}
					}
				});						
			});
		});
		$('#id_form-'+cpt+'-departure_country').on('change', function(){
			p = $(this).val();
			$.getJSON('../../../static/json/pays.json', function(data){
				$('#id_form-'+cpt+'-departure_city').empty();
				$.each(data, function(index, d){
					if(d.code == p){
						for (i = 0; i < d.villes.length; i++) {
							if (city == d.villes[i]) {
								$('#id_form-'+cpt+'-departure_city').append('<option selected value=\'' + d.villes[i] + '\'>' + d.villes[i] + '</option>');
							 } else{
								 $('#id_form-'+cpt+'-departure_city').append('<option value=\'' + d.villes[i] + '\'>' + d.villes[i] + '</option>');
							 }
						}
					}
				});
			});
		});
	}
}

/** for destinations */
function load_dest_place(){
	for(let cpt=0; cpt<2; cpt++) {
		var i, p, valeur;
		$.getJSON('../../../static/json/pays.json', function(data){
			$('#id_form-'+cpt+'-destination_country').empty();
			$('#id_form-'+cpt+'-destination_city').empty();
			$('#id_form-'+cpt+'-destination_country').append("<option value=''>----------</option>");
			$('#id_form-'+cpt+'-destination_city').append("<option value=''>----------</option>");
			$.each(data, function(index, d){
				$('#id_form-'+cpt+'-destination_country').append('<option value=\'' + d.code + '\'>' + d.pays + '</option>');
				valeur = $('#id_form-'+cpt+'-destination_country').val();
				$.each(data, function(index, d){
					if(valeur == d.pays){
						$('#id_form-'+cpt+'-destination_city').empty();
						for (i = 0; i < d.villes.length; i++) {
							$('#id_form-'+cpt+'-destination_city').append('<option value=\'' + d.villes[i] + '\'>' + d.villes[i] + '</option>');
						}
					}
				});						
			});
		});
		$('#id_form-'+cpt+'-destination_country').on('change', function(){
			p = $(this).val();
			$.getJSON('../../../static/json/pays.json', function(data){
				$('#id_form-'+cpt+'-destination_city').empty();
				$.each(data, function(index, d){
					if(d.code == p){
						for (i = 0; i < d.villes.length; i++) {
							$('#id_form-'+cpt+'-destination_city').append('<option value=\'' + d.villes[i] + '\'>' + d.villes[i] + '</option>');
						}
					}
				});
			});
		});
	}
}


function load_departure_place(country, city){
	var i, p, valeur;
	$.getJSON('../../../static/json/pays.json', function(data){
		$('#id_departure_country').empty();
		$('#id_departure_city').empty();
		$('#id_departure_country').append("<option value=''>----------</option>");
		$('#id_departure_city').append("<option value=''>----------</option>");
		$.each(data, function(index, d){
			if (country == d.code) {
				$('#id_departure_country').append('<option selected value=\'' + d.code + '\'>' + d.pays + '</option>');
			} else{
				$('#id_departure_country').append('<option value=\'' + d.code + '\'>' + d.pays + '</option>');
			}
			valeur = $('#id_departure_country').val();
			$.each(data, function(index, d){
				if(valeur == d.pays){
					$('#id_departure_city').empty();
					for (i = 0; i < d.villes.length; i++) {
						if (city == d.villes[i]) {
						   $('#id_departure_city').append('<option selected value=\'' + d.villes[i] + '\'>' + d.villes[i] + '</option>');
						} else{
							$('#id_departure_city').append('<option value=\'' + d.villes[i] + '\'>' + d.villes[i] + '</option>');
						}
					}
				}
			});						
		});
	});
	$('#id_departure_country').on('change', function(){
		p = $(this).val();
		$.getJSON('../../../static/json/pays.json', function(data){
			$('#id_departure_city').empty();
			$.each(data, function(index, d){
				if(d.code == p){
					for (i = 0; i < d.villes.length; i++) {
						if (city == d.villes[i]) {
							$('#id_departure_city').append('<option selected value=\'' + d.villes[i] + '\'>' + d.villes[i] + '</option>');
						 } else{
							 $('#id_departure_city').append('<option value=\'' + d.villes[i] + '\'>' + d.villes[i] + '</option>');
						 }
					}
				}
			});
		});
	});
}

/** for destinations */
function load_destination_place(){
	var i, p, valeur;
	$.getJSON('../../../static/json/pays.json', function(data){
		$('#id_destination_country').empty();
		$('#id_destination_city').empty();
		$('#id_destination_country').append("<option value=''>----------</option>");
		$('#id_destination_city').append("<option value=''>----------</option>");
		$.each(data, function(index, d){
			$('#id_destination_country').append('<option value=\'' + d.code + '\'>' + d.pays + '</option>');
			valeur = $('#id_destination_country').val();
			$.each(data, function(index, d){
				if(valeur == d.pays){
					$('#id_destination_city').empty();
					for (i = 0; i < d.villes.length; i++) {
   						$('#id_destination_city').append('<option value=\'' + d.villes[i] + '\'>' + d.villes[i] + '</option>');
					}
				}
			});						
		});
	});
	$('#id_destination_country').on('change', function(){
		p = $(this).val();
		$.getJSON('../../../static/json/pays.json', function(data){
			$('#id_destination_city').empty();
			$.each(data, function(index, d){
				if(d.code == p){
					for (i = 0; i < d.villes.length; i++) {
						$('#id_destination_city').append('<option value=\'' + d.villes[i] + '\'>' + d.villes[i] + '</option>');
					}
				}
			});
		});
	});
}

// filtres of the departure and destintion country
// My function 1
function load_departure_place1(country, city, cpt){
	var i, p, valeur;
	$.getJSON('../../../static/json/pays.json', function(data){
		$('#id_form-'+cpt+'-departure_country').empty();
		$('#id_form-'+cpt+'-departure_city').empty();
		$('#id_form-'+cpt+'-departure_country').append("<option value=''>----------</option>");
		$('#id_form-'+cpt+'-departure_city').append("<option value=''>----------</option>");
		$.each(data, function(index, d){
			if (country == d.code) {
				$('#id_form-'+cpt+'-departure_country').append('<option selected value=\'' + d.code + '\'>' + d.pays + '</option>');
			} else{
				$('#id_form-'+cpt+'-departure_country').append('<option value=\'' + d.code + '\'>' + d.pays + '</option>');
			}
			valeur = $('#id_form-'+cpt+'-departure_country').val();
			$.each(data, function(index, d){
				if(valeur == d.code){
					$('#id_form-'+cpt+'-departure_city').empty();
					for (i = 0; i < d.villes.length; i++) {
						if (city == d.villes[i]) {
						   $('#id_form-'+cpt+'-departure_city').append('<option selected value=\'' + d.villes[i] + '\'>' + d.villes[i] + '</option>');
						} else{
							$('#id_form-'+cpt+'-departure_city').append('<option value=\'' + d.villes[i] + '\'>' + d.villes[i] + '</option>');
						}
					}
				}
			});						
		});
	});
	$('#id_form-'+cpt+'-departure_country').on('change', function(){
		p = $(this).val();
		$.getJSON('../../../static/json/pays.json', function(data){
			$('#id_form-'+cpt+'-departure_city').empty();
			$.each(data, function(index, d){
				if(d.code == p){
					for (i = 0; i < d.villes.length; i++) {
						if (city == d.villes[i]) {
							$('#id_form-'+cpt+'-departure_city').append('<option selected value=\'' + d.villes[i] + '\'>' + d.villes[i] + '</option>');
						 } else{
							 $('#id_form-'+cpt+'-departure_city').append('<option value=\'' + d.villes[i] + '\'>' + d.villes[i] + '</option>');
						 }
					}
				}
			});
		});
	});
}


// My function 2

function load_destination_place1(country, city, cpt){
	var i, p, valeur;
	$.getJSON('../../../static/json/pays.json', function(data){
		$('#id_form-'+cpt+'-destination_country').empty();
		$('#id_form-'+cpt+'-destination_city').empty();
		$('#id_form-'+cpt+'-destination_country').append("<option value=''>----------</option>");
		$('#id_form-'+cpt+'-destination_city').append("<option value=''>----------</option>");
		$.each(data, function(index, d){
			if (country == d.code) {
				$('#id_form-'+cpt+'-destination_country').append('<option selected value=\'' + d.code + '\'>' + d.pays + '</option>');
			} else{
				$('#id_form-'+cpt+'-destination_country').append('<option value=\'' + d.code + '\'>' + d.pays + '</option>');
			}
			valeur = $('#id_form-'+cpt+'-destination_country').val();
			$.each(data, function(index, d){
				if(valeur == d.code){
					$('#id_form-'+cpt+'-destination_city').empty();
					for (i = 0; i < d.villes.length; i++) {
						if (city == d.villes[i]) {
						   $('#id_form-'+cpt+'-destination_city').append('<option selected value=\'' + d.villes[i] + '\'>' + d.villes[i] + '</option>');
						} else{
							$('#id_form-'+cpt+'-destination_city').append('<option value=\'' + d.villes[i] + '\'>' + d.villes[i] + '</option>');
						}
					}
				}
			});						
		});
	});
	$('#id_form-'+cpt+'-destination_country').on('change', function(){
		p = $(this).val();
		$.getJSON('../../../static/json/pays.json', function(data){
			$('#id_form-'+cpt+'-destination_city').empty();
			$.each(data, function(index, d){
				if(d.code == p){
					for (i = 0; i < d.villes.length; i++) {
						if (city == d.villes[i]) {
							$('#id_form-'+cpt+'-destination_city').append('<option selected value=\'' + d.villes[i] + '\'>' + d.villes[i] + '</option>');
						 } else{
							 $('#id_form-'+cpt+'-destination_city').append('<option value=\'' + d.villes[i] + '\'>' + d.villes[i] + '</option>');
						 }
					}
				}
			});
		});
	});
}