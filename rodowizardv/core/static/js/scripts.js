
    function check_third(event){
        console.log('in third');
        if(!(document.getElementById("id_street").checkValidity() && 
                document.getElementById("id_post_code").checkValidity() &&
                    document.getElementById("id_city").checkValidity()))
            {
                document.getElementById("id_street").reportValidity();
                document.getElementById("id_post_code").reportValidity();
                document.getElementById("id_city").reportValidity();
                event.stopPropagation();
                event.preventDefault();
                event.cancelBubble = true;
                event.stopImmediatePropagation();
            }
        else{
            fourth();
        }
    }

    function check_first(event){
        console.log('in check_first');
        if(!(document.getElementById("id_name").checkValidity() && 
            document.getElementById("id_surname").checkValidity()))
            {
                document.getElementById("id_name").reportValidity();
                document.getElementById("id_surname").reportValidity();
                event.stopPropagation();
                event.preventDefault();
                event.cancelBubble = true;
                event.stopImmediatePropagation();
            }
        else{
            second();
        }
    }

    function check_second(event){
        console.log('in check_second');
        if(!(document.getElementById("id_email").checkValidity() && 
            document.getElementById("id_phone_number").checkValidity()))
            {
                document.getElementById("id_email").reportValidity();
                document.getElementById("id_phone_number").reportValidity();
                event.stopPropagation();
                event.preventDefault();
                event.cancelBubble = true;
                event.stopImmediatePropagation();
            }
        else{
            third();
        }
    }

    function first(event){
        console.log('in first');
        $("#1").css('color', 'green');
        $("#2").css('color', 'gray');
        $("#3").css('color', 'gray');
        $("#4").css('color', 'gray');
    
        $("#name-surname").show();
        $("#address-details").hide();
        $("#street-post-city").hide();
        $("#summary").hide();
        $("#submit").hide();
        $("#next").show();

        $("#next").on('click', check_first);
    }
    

    function second(event){
        console.log('in second');
        $("#1").css('color', 'gray');
        $("#2").css('color', 'green');
        $("#3").css('color', 'gray');
        $("#4").css('color', 'gray');

        $("#name-surname").hide();
        $("#address-details").show();
        $("#street-post-city").hide();
        $("#summary").hide();
        $("#submit").hide();
        $("#next").show();

        $("#next").on('click', check_second);
    }

    function third(event){
        console.log('in third');
        $("#1").css('color', 'gray');
        $("#2").css('color', 'gray');
        $("#3").css('color', 'green');
        $("#4").css('color', 'gray');

        $("#name-surname").hide();
        $("#address-details").hide();
        $("#street-post-city").show();
        $("#summary").hide();
        $("#submit").hide();
        $("#next").show();

        $("#next").on('click', check_third);
    }

    function fourth(){
        console.log('in fourth');
        $("#1").css('color', 'gray');
        $("#2").css('color', 'gray');
        $("#3").css('color', 'gray');
        $("#4").css('color', 'green');

        $("#name-surname").hide();
        $("#address-details").hide();
        $("#street-post-city").hide();
        $("#summary").show();
        $("#submit").show();
        $("#next").hide();
    }

    function init(event){
        first(event);
        $("#block_1").on('click', function(event){
            first(event);
        });
        $("#block_2").on('click', function(event){
            second(event);
        });
        $("#block_3").on('click', function(event){
            third(event);
        });
        $("#block_4").on('click', function(event){
            fourth(event);
        });
    }

    $(window).on('load', function(event) {
        init(event);
    });

    $(document).ready(function(event){
        init(event);
        var post_code_regex = /^\d{2}-\d{3}$/;
        var phone_number_regex = /^\+?[\d\-\s]{9,20}$/;
        document.getElementById("id_post_code").setAttribute(
            "pattern", post_code_regex.source);
        document.getElementById("id_phone_number").setAttribute(
            "pattern", phone_number_regex.source)
    });

