// general stuff, always loaded

// hide the generic errors
$('#confirm-flash').hide();
$('#alert-flash').hide();

$('.confirm').on('click', function (event) {
    // remove all visible alerts
    $('.alert-dismissible').remove();
    // set confirmation url for confirmation button to the action
    $('#confirm-true').data('action_href', $(this).data('confirm'));
    // show the button
    $('#confirm-flash').show();
});

$('.confirm-false').on('click', function (event) {
    console.log("false");
    // hide the button
    $('#confirm-flash').hide();
    $('#confirm-true').data('action_href', '');
});

var csrftoken = $('meta[name=csrf-token]').attr('content');

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$('#confirm-true').on('click', function (event) {
    //console.log("true");
    var this_href = $('#confirm-true').data('action_href');
    var this_url =  $SCRIPT_ROOT + this_href;
    // TODO handle result or replace?
    window.location.replace(this_url);
    /*
    $.ajax({
      type: 'GET',
      url: $SCRIPT_ROOT + this_href,
      dataType: 'json'
      })
      .success(function(ret) {
        console.log('Success');
        showSuccess(ret);
      })
      .done(function (ret) {
        $('#confirm-flash').hide();
        console.log('Done');
      })
      .fail(function (ret) {
        console.log('fail');
        showError(ret.responseText);
      });
    */
});
/*
*/

/*
$('#deleteConfirmed').on('click', function (event) {
    //alert($(this).data('onConfirm'));
});
*/

function _setMessage(message, this_type){
    $('#alert-flash').hide();
    $('#confirm-flash').hide();
    $('#alert-flash').removeClass('bg-danger', 'bg-primary', 'bg-success');
    $('#alert-flash').addClass(this_type);
    $('#alert-flash').html(message);
    $('#alert-flash').show();
}

function showError(message){
    return _setMessage(message, 'bg-danger');
}

function showNotice(message){
    return _setMessage(message, 'bg-primary');
}

function showSuccess(message){
    return _setMessage(message, 'bg-success');
}

