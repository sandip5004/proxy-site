$(document).ready(function () {
    $.ajaxSetup({
        beforeSend: function (xhr) {
            xhr.setRequestHeader('x-my-custom-header', 'some value');
        }
    });
    $(".clickable-row").click(function () {
        window.location = $(this).data("href");
    });
    $('#dtBasicExample').DataTable({"scrollX": true});
    $('.dataTables_length').addClass('bs-select');
    $(function () {
        $('[data-toggle="tooltip"]').tooltip();
    });
});

var ajaxCall = function (type, url, callback, func_type, formData = '') {
    $.ajax({
        url: url,
        type: type.toUpperCase(),
        data: formData,
        cache: false,
        async: true,
        contentType: false,
        processData: false,
        success: function (data, textStatus, xhr) {
            if ($.isFunction(callback))
                callback(data, 'success', func_type, xhr);
        },
        error: function (data, textStatus, xhr) {
            if ($.isFunction(callback))
                callback(data, 'error', func_type, xhr);
        }
    });
};

class LmsAdminUtils {
    constructor() {
    }

    loader(type = 'show') {
        if(type==='show') {
            $('#modalCreateEditForm').modal('show');
            $('#modalCreateEditForm .modal-content').html($('.loader').html());
        }
        else {
            $('#modalCreateEditForm').modal('hide');
            $('#modalCreateEditForm .modal-content').html('');
        }
    }

    handleResponse(data, type, func_type, xhr) {
        try {
            if (type === 'success')
                LmsAdminObj[func_type](data);
            else
                LmsAdminObj['error_' + func_type](data);
        }
        catch (e) {
            console.log("Exception: handleResponse");
            console.log(e);
        }
    }

    loadModuleData(method, obj) {
        try {
            var url = $(obj).attr('data-href');
            var func_type = $(obj).attr('func-type');
            LmsAdminObj.loader('show');
            ajaxCall(method, url, LmsAdminObj.handleResponse, func_type);
        }
        catch (e) {
            console.log("Exception: handleResponse");
            console.log(e);
        }
    }

    deleteModuleData(method, obj) {
        try {
            var url = $(obj).attr('data-href');
            var title = $(obj).attr('data-msg-title');
            var description = $(obj).attr('data-msg-description');
            var func_type = $(obj).attr('func-type');
            swal({
                title: title,
                text: description,
                icon: "warning",
                buttons: true,
                dangerMode: true,
            })
                .then((willDelete) => {
                    if (willDelete) {
                        ajaxCall(method, url, LmsAdminObj.handleResponse, func_type);
                    }
                });
        }
        catch (e) {
            console.log("Exception: handleResponse");
            console.log(e);
        }
    }

    loadDeleteRecord(response) {
        try {
            console.log(response);
            $('#modalCreateEditForm .modal-content').html(response);
        }
        catch (e) {
            console.log("Exception: handleResponse");
            console.log(e);
        }
    }

    error_loadDeleteRecord(response) {
        try {
            $('#modalCreateEditForm').modal('hide');
            console.log(response);
            $('#errorModal h4').text(response.statusText);
            $('#errorModal .modal-body').text(response.responseText);
            $('#errorModal').modal('show');
        }
        catch (e) {
            console.log("Exception: error_loadEditRecordForm");
            console.log(e);
        }
    }

    loadEditRecordForm(response) {
        try {
            console.log(response);
            $('#modalCreateEditForm .modal-content').html(response);
        }
        catch (e) {
            console.log("Exception: handleResponse");
            console.log(e);
        }

    }

    error_loadEditRecordForm(response) {
        try {
            $('#modalCreateEditForm').modal('hide');
            console.log(response);
            $('#errorModal h4').text(response.statusText);
            $('#errorModal .modal-body').text(response.responseText);
            $('#errorModal').modal('show');
        }
        catch (e) {
            console.log("Exception: error_loadEditRecordForm");
            console.log(e);
        }
    }

    saveEditForm(response) {
        try {
            console.log(response);
            $('.server-response-message').html(response.msg);
        }
        catch (e) {
            console.log("Exception: saveEditForm");
            console.log(e);
        }
    }

    error_saveEditForm(response) {
        try {
            $('.server-response-message').html('');
            console.log(response);
            $.each(response.responseJSON, function (field, value_obj) {
                if ($.isEmptyObject(value_obj.error)) {
                }
                else {
                    $('#' + field + '--error').text(value_obj.error);
                    $('#' + field + '--error').removeClass('hidden');
                }
            });
        }
        catch (e) {
            console.log("Exception: error_saveEditForm");
            console.log(e);
        }
    }
}

LmsAdminObj = new LmsAdminUtils();