Dropzone.autoDiscover = false;

$(() => {
    var myDropzone = new Dropzone('#dropzone');
    Dropzone.options.myDropzone = {
        maxFiles: 1,
        autoProcessQueue: false,
    };
    myDropzone.on('addedfiles', (files) => {
        const numFiles = files.length;
        if (numFiles > 1) {
            window.location = "{{ url_for('error_.error', error_type='more_than_one_file') }}";
        }
    });
    myDropzone.on('success', (file, response) => {
        const parsedResponse = JSON.parse(response);
        if (parsedResponse.success === true) {
            window.location = "{{ url_for('upload_.upload', file_uploaded=True) }}";
        } else {
            window.location = "{{ url_for('error_.error', error_type='ERROR_TYPE_HERE') }}".replace('ERROR_TYPE_HERE', parsedResponse.error);
        }
    });
});
