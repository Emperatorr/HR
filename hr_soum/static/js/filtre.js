$(function(){
	var i, p, valeur;
	$.getJSON('../../static/json/pays.json', function(data){
		$('#id_mission_country').empty();
		$('#id_mission_city').empty();
		$('#id_mission_country').append("<option value=''>----------</option>");
		$('#id_mission_city').append("<option value=''>----------</option>");
		$.each(data, function(index, d){
			$('#id_mission_country').append('<option value=\'' + d.code + '\'>' + d.pays + '</option>');
			valeur = $('#id_mission_country').val();
			$.each(data, function(index, d){
				if(valeur == d.code){
					$('#id_mission_city').empty();
					for (i = 0; i < d.villes.length; i++) {
   						$('#id_mission_city').append('<option value=\'' + d.villes[i] + '\'>' + d.villes[i] + '</option>');
					}
				}
			});						
		});
	});
	$('#id_mission_country').on('change', function(){
		p = $(this).val();
		$.getJSON('../../static/json/pays.json', function(data){
			$('#id_mission_city').empty();
			$.each(data, function(index, d){
				if(d.code == p){
					for (i = 0; i < d.villes.length; i++) {
						$('#id_mission_city').append('<option value=\'' + d.villes[i] + '\'>' + d.villes[i] + '</option>');
					}
				}
			});
		});
	});
});
