$(".submit").click(function(e){
    $('#cargandomodal').modal({
    backdrop: 'static',
    keyboard: false
    });
    $('#cargandomodal').modal('show');
    
});
function init_selected_class_name(class_name,selected){
    if(selected == "all" || selected == "None"){
        $("."+class_name+".option").addClass("selected-option");
    }else{
        $("."+class_name+".option").each(function(){
            if(selected.includes($(this).text())){
                $(this).addClass("selected-option");
            }
        });
    }
    get_selected_num(class_name);
}
function get_selected_num(class_name)
{
    let selected_province_num = $("."+class_name + '.option-default.selected-option').length
    if (selected_province_num == $("."+class_name+".option-default").length){
        $("#"+class_name+"-dropdown-button").text("Todas");
        $("."+class_name + ".all-option").addClass("selected-option");
        console.log("todas!!");
    }
    else{
        let text = selected_province_num + " seleccionadas";
        if(selected_province_num == 1){
            text = selected_province_num + " seleccionada";
        }
        $("#"+class_name+"-dropdown-button").text(text);
        $("."+class_name + ".all-option").removeClass("selected-option");
        console.log(selected_province_num);
        console.log( $("."+class_name).length)
    }
}
/*
function get_selected_num()
{
    let selected_province_num = $('.province-option-default.selected-option').length
    if (selected_province_num == $(".province-option-default").length){
        $("#dropdownMenuButton1").text("Todas");
        $(".all-option").addClass("selected-option");
    }
    else{
        let text = selected_province_num + " seleccionadas";
        if(selected_province_num == 1){
            text = selected_province_num + " seleccionada";
        }
        $("#dropdownMenuButton1").text(text);
        $(".all-option").removeClass("selected-option");
    }
}
*/
function select_default_option(class_name){
    $("."+class_name+".option-default").click(function(e){
        e.preventDefault();
        e.stopPropagation();
        console.log($(this).text());
        $(this).toggleClass("selected-option");
        $("."+class_name+".all-option").removeClass("selected-option");
        $("."+class_name+".option-input").val('');
        
        $("."+class_name+".option").show();
        get_selected_num(class_name);
    
    });
}
/*
$(".province-option-default").click(function(e){
    e.preventDefault();
    e.stopPropagation();
    console.log($(this).text());
    $(this).toggleClass("selected-option");
    $(".all-option").removeClass("selected-option");
    $(".option-input").val('');
    province_filter="";
    $(".province-option").show();
    get_selected_num();

});
*/
function select_all_option(class_name){
    $("."+class_name+".all-option").click(function(e){
        e.preventDefault();
        e.stopPropagation();
        console.log($(this).text());
        $(this).toggleClass("selected-option");
        if($(this).hasClass("selected-option")){   
            $("."+class_name+".option-default").addClass("selected-option");
            get_selected_num(class_name);
        }
        else{
            $("."+class_name+".option-default").removeClass("selected-option");
            $("#"+class_name+"-dropdown-button").text("0 seleccionadas");
        }
    });
}
/*
$(".all-option").click(function(e){
    e.preventDefault();
    e.stopPropagation();
    console.log($(this).text());
    $(this).toggleClass("selected-option");
    if($(this).hasClass("selected-option")){   
        $(".province-option-default").addClass("selected-option");
        get_selected_num();
    }
    else{
        $(".province-option-default").removeClass("selected-option");
        $("#dropdownMenuButton1").text("0 seleccionadas");
    }
    
});
*/
function input_key_up(class_name){
    $("."+class_name+".option-input").keyup(function(e){
        if(e.keyCode == 13){
            e.preventDefault();
            e.stopPropagation();
            console.log($(this).val());
            //$(this).parent().addClass("selected-option");
        }
        else{
            filter = $(this).val() ;
            if(filter.length > 1){
                $("."+class_name+".option").each(function(index,element){
                if($(element).text().toLowerCase().includes(filter.toLowerCase())){
                    $(element).show();
                }
                else{
                    $(element).hide();
                }
            });
            }
            else{
                $("."+class_name+".option").show();
            }
            
        }
    });
}
/*
$(".option-input").on("keyup",function(e){
    if(e.keyCode == 13){
        e.preventDefault();
        e.stopPropagation();
        console.log($(this).val());
        //$(this).parent().addClass("selected-option");
    }
    else{
        province_filter = $(this).val() ;
        if(province_filter.length > 1){
            $(".province-option").each(function(index,element){
            if($(element).text().toLowerCase().includes(province_filter.toLowerCase())){
                $(element).show();
            }
            else{
                $(element).hide();
            }
        });
        }
        else{
            $(".province-option").show();
        }
        
    }
});
*/
function get_selected(class_name)
{
    let selected_array = [];
    if($("."+class_name+".all-option").hasClass("selected-option")){
        selected_array.push("all");
    }
        else{
            $("."+class_name+".option-default").each(function(index,element){
                if($(element).hasClass("selected-option")){
                    selected_array.push($(element).text());
                }
            });
        }
        let selected_str = selected_array.join(",");
        $("#"+class_name+"-input").val(selected_str);
}

function submit_form(class_names){
    $("#form-submit").click(function(e){
        // for class_name in class_names:
        //     get_selected(class_name);
        for (let i = 0; i < class_names.length; i++) {
            get_selected(class_names[i]);
        }
    });
}
function start(class_names){
    for (let i = 0; i < class_names.length; i++) {
        select_default_option(class_names[i]);
        select_all_option(class_names[i]);
        input_key_up(class_names[i]);

    }
    submit_form(class_names);
}
/*
$("#form-submit").click(function(e){
    //e.preventDefault();

    //e.stopPropagation();
    let provinces_array = [];
    if($(".all-option").hasClass("selected-option")){
        provinces_array.push("all");
    }
    else{
        $(".province-option-default").each(function(index,element){
            if($(element).hasClass("selected-option")){
                provinces_array.push($(element).text());
            }
        });
    }
    let provinces_str = provinces_array.join(",");
    $("#provinces-input").val(provinces_str);
});
*/
