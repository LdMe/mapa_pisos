var prices;

// get bins and labels from api with ajax
$.ajax({
    url: "/api/v1/bins",
    type: "GET",
    success: function(data){
        var bins = data.bins;
        var labels = data.labels;
        // add options for id surface-select 
        for (var i = 0; i < labels.length; i++) {
            var option = document.createElement("option");
            option.value = bins[i];
            option.text = labels[i];
            // get value of surface from url using only javascript
            var url = new URL(window.location.href);
            var surface = url.searchParams.get("surface");
            // if bin in surface is equal to the bin in the api, select the option
            if (option.value == surface){
                option.selected = true;
            }
            document.getElementById("surface-select").appendChild(option);
            
        }
    },
    error: function(error){
        console.log(error);
    }
});
$.ajax({
    url: "/api/v1/dates",
    type: "GET",
    success: function(data){
        var dates = data.dates;
        // reverse array
        dates = dates.reverse();
        console.log(dates);

        for (var i = 0; i < dates.length; i++) {
            var option = document.createElement("option");
            option.value = dates[i][0]+"/"+dates[i][1];
            option.text = dates[i][0]+"/"+dates[i][1];
            option.className = "dropdown-item dates option option-default pt-2";
            
            document.getElementById("dates-list").appendChild(option);
        }
        init_selected_class_name("dates");
        start_class("dates");

    },
    error: function(error){
        console.log(error);
    }

});
$.ajax({
    url: "/api/v1/provinces",
    type: "GET",
    success: function(data){
        var provinces = data.provinces;
        console.log(provinces);

        for (var i = 0; i < provinces.length; i++) {
            var option = document.createElement("option");
            option.value = provinces[i];
            option.text = provinces[i];
            option.className = "dropdown-item provinces option option-default pt-2";
            
            document.getElementById("provinces-list").appendChild(option);
        }
        init_selected_class_name("provinces");
        start_class("provinces");

    },
    error: function(error){
        console.log(error);
    }

});
function toggle(class_name){
    $("#"+class_name+"-outside").toggle();
    $("#"+class_name+"-down").toggle();
    $("#"+class_name+"-up").toggle();
}
$("#price-show").click(function(){
    toggle("price");
});
$("#graph-show").click(function(){
    toggle("graph");
});
$("#bars-show").click(function(){
    toggle("bars");
});
$("#price").click(function(e){
    e.stopPropagation();
});
$("#graph").click(function(e){
    e.stopPropagation();
});
$("#bars").click(function(e){
    e.stopPropagation();
});
$("#price-down").hide();
$("#graph-down").hide();
$("#bars-down").hide();

$("#price-load").hide();
$("#graph-load").hide();
$("#bars-load").hide();

toggle("price");
toggle("graph");
toggle("bars");
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
    e.stopPropagation();
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
    e.stopPropagation();
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

function init_selected_class_name(class_name){
    $("."+class_name+".option").addClass("selected-option");
    
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
    $("#price").html(html);
}

function submit_form(class_names){
    $("#form-submit").click(function(e){
        e.preventDefault();
        e.stopPropagation();
        // for class_name in class_names:
        //     get_selected(class_name);
        for (let i = 0; i < class_names.length; i++) {
            get_selected(class_names[i]);
        }
        $("#price-load").show();
        $form_data = $("#properties-form").serialize();
        
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
function start_class(class_name){
    select_default_option(class_name);
    select_all_option(class_name);
    input_key_up(class_name);
}
function start(class_names){
    
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
