$(document).ready(function () {
    $('.image-section').hide();
    $('.loader').hide();
    $('#result').hide();
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
    $("#imageUpload").change(function () {
        $('.image-section').show();
        $('#btn-predict').show();
        $('#result').text('');
        $('#result').hide();
        readURL(this);
    });
    $('#btn-predict').click(function () {
        var form_data = new FormData($('#upload-file')[0]);
        $(this).hide();
        $('.loader').show();
        $('#topk').empty();
        $('#similar').empty();
        $('#result').empty();
        $('#link').empty();

        $.ajax({
            type: 'POST',
            url: '/predict',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            dataType: 'json',
            async: true,
            success: function (data) {
                $('.loader').hide();
                $('#result').fadeIn(600);
                $('#result').text(' Result:  ' + data.preds);
                $('#link').append("<a href= '" + data.links + "\'>"+ data.links + "</a >")
                $('#topkTitle').text("Dominant colors: ");
                $('#similarTitle').text("Similar products: ");
                var images = data.imgs
                for (var i=0; i < images.length; i++){
                    console.log(images[i]);
                    if(images[i].endsWith('topk.jpg')){
                      $('#topk').append("<li><img src=\'" + images[i] + "\' alt=\"\" width=\"200\" height=\"150\" /></li>");
                    }
                }
                var images = data.imgs
                for (var i=0; i < images.length; i++){
                  if(!images[i].endsWith('topk.jpg')){
                    $('#similar').append("<li><img src=\'" + images[i] + "\' alt=\"\" width=\"200\" height=\"150\" /></li>");
                  }
                }
                console.log(data);
            },
        });
    });

});
