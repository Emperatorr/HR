jQuery(document).ready(function($){
	$('input').click(function(){
		$('.alert').hide();
		$('.has-error').removeClass();
		$('.help-block').hide();
		$('.form-group').css('margin-bottom', '10px');
	});
	$('#id_approved').click(function(){
		if ($(this).is(':checked')) {
			$('#why_not_approved').hide();
		} else {
			$('#why_not_approved').show();
		}
	});
	$('#flight_type').hide();
	$('#class_type').hide();
	$('#flight_price').hide();
	$('#date').hide()
	$('#id_flight_available').click(function(){
		if ($(this).is(':checked')) {
			$('#flight_type').show();
			$('#class_type').show();
			$('#flight_price').show();
			$('#date').show()
			$('#id_flight_not_available').prop('disabled', true);
		} else {
			$('#flight_type').hide();
			$('#class_type').hide();
			$('#flight_price').hide();
			$('#date').hide();
			$('#id_flight_not_available').prop('disabled', false);
		}
	});
	$('#id_flight_not_available').click(function(){
		if ($(this).is(':checked')) {
			$('#id_flight_available').prop('disabled', true);
		} else {
			$('#id_flight_available').prop('disabled', false);
		}
	})
	$('#flight1').click(function(){
		if ($(this).is(':checked')) {
			$('#flight2').prop('disabled', true);
			$('#flight3').prop('disabled', true);
		} else {
			$('#flight2').prop('disabled', false);
			$('#flight3').prop('disabled', false);
		}
	});
	$('#flight2').click(function(){
		if ($(this).is(':checked')) {
			$('#flight1').prop('disabled', true);
			$('#flight3').prop('disabled', true);
		} else {
			$('#flight1').prop('disabled', false);
			$('#flight3').prop('disabled', false);
		}
	});
	$('#flight3').click(function(){
		if ($(this).is(':checked')) {
			$('#flight1').prop('disabled', true);
			$('#flight2').prop('disabled', true);
		} else {
			$('#flight1').prop('disabled', false);
			$('#flight2').prop('disabled', false);
		}
	});
});
