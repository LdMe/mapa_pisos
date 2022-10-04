var prices;
$(".submit").click(function(e){
    /*
    $('#cargandomodal').modal({
    backdrop: 'static',
    keyboard: false
    });
    
    $('#cargandomodal').modal('show');
    */
});

$("#graph-button").click(function(e){
    $("#graph-load").show();
    //console.log(prices);
    $.ajax({
        url: "/api/v1/graph",
        type: "POST",
        data: prices,
        contentType: "application/json",
        success: function(data){
            plotGraph(graphs=JSON.parse(data));
            $("#graph-load").hide();
        },
        error: function(data){
            console.log(data);
            $("#graph-load").hide();
        }
    });
    return;
    $('#cargandomodal').modal('show');
    
});
$("#bars-button").click(function(e){
    $("#bars-load").show();
    $.ajax({
        url: "/api/v1/bars",
        type: "POST",
        data: prices,
        contentType: "application/json",
        success: function(data){
            
            plotGraph(graphs=null,barras=JSON.parse(data));
            $("#bars-load").hide();
        },
        error: function(){
            $("#bars-load").hide();
        }
    });

    return;
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
        
    }
    else{
        let text = selected_province_num + " seleccionadas";
        if(selected_province_num == 1){
            text = selected_province_num + " seleccionada";
        }
        $("#"+class_name+"-dropdown-button").text(text);
        $("."+class_name + ".all-option").removeClass("selected-option");
        
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
function create_html_table(data){
    let html = "<table class='table table-striped table-bordered table-hover table-sm'>";
    html += "<thead class='thead-dark'><tr>";
    for (let key in data[0]) {
        html += "<th>"+key+"</th>";
    }
    html += "</tr></thead>";
                // get body
    html += "<tbody>";
    for (let i = 0; i < data.length; i++) {
        html += "<tr>";
        for (let key in data[i]) {
            html += "<td>"+data[i][key]+"</td>";
        }
        html += "</tr>";
    }
    html += "</tbody>";
    html += "</table>";
    $("#price-table").html(html);
}

function submit_form(class_names){
    $("#form-submit").click(function(e){
        // for class_name in class_names:
        //     get_selected(class_name);
        for (let i = 0; i < class_names.length; i++) {
            get_selected(class_names[i]);
        }
        $("#price-load").show();
        $form_data = $("#properties-form").serialize();
        e.preventDefault();
        //e.stopPropagation();
        $.ajax({
            url: "/api/v1/predict?"+$form_data,
            type: "GET",
            success: function(data){
                prices = data;
                data = JSON.parse(data);
                create_html_table(data);

            },
            complete: function(){
                $("#price-load").hide();
            }

        });

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
