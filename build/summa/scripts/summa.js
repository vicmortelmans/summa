// Smooth scrolling
$(document).on('click', 'a[href^="#"]:not(#nav-toggle, .nav-secondary-toggle, .nav-ternary-toggle)', function (event) {
      $('html, body').animate({
          scrollTop: $($.attr(this, 'href')).offset().top - 67
      }, 500);
});

$(function(){
    // Primary nav toggle
    $("#nav-toggle").on("touch click", function(){
        if ($("body").hasClass("locked"))
            $("body").removeClass("locked");
        else
            $("body").addClass("locked");
        
        $("#nav-primary").toggleClass("open");
        $("#nav-secondary").removeClass("open");
        $("#nav-ternary").removeClass("open");
        return false;
    });
    
    // Secondary nav toggle
    $("#nav-secondary-toggle").on("touch click", function(){
        if ($("body").hasClass("locked"))
            $("body").removeClass("locked");
        else
            $("body").addClass("locked");
        $("#nav-secondary").toggleClass("open");
        $("#nav-primary").removeClass("open");
        $("#nav-ternary").removeClass("open");
        return false;
    });
    
    // Ternary nav toggle
    $("#nav-ternary-toggle").on("touch click", function(){
        if ($("body").hasClass("locked"))
            $("body").removeClass("locked");
        else
            $("body").addClass("locked");
        $("#nav-ternary").toggleClass("open");
        $("#nav-primary").removeClass("open");
        $("#nav-secondary").removeClass("open");
        return false;
    });
    
    $("#nav-secondary a").on("touch click", function(){
        $("body").removeClass("locked");
        $("#nav-secondary").removeClass("open");
    });
    
    $("#nav-ternary a").on("touch click", function(){
        $("body").removeClass("locked");
        $("#nav-ternary").removeClass("open");
    });
    
    // Wrap parenthesis in problem statements to reverse italicization
    $(".problem").each(function(){
        $(this).html($(this).html().trim().replace(/([\(\){}])/gi, "<span class='norm'>$1</span>"));
    });
    
    // Wrap first words
    $(".dropcap").each(function(){
        if ($(this).html().trim().length > 0) {
            var firstWord = $(this).html().trim().match(/^(\w+)/)[0];
            
            if (firstWord.length > 1) {
                // Wrap first word
                $(this).html($(this).html().trim().replace(/^(\w+)/, "<span class='first-word'>$1</span>"));
            } else {
                // Wrap first two words
                $(this).html($(this).html().trim().replace(/^([^\s]*) ([^\s]*)/, "<span class='first-word'>$1 $2</span>"));
            }
        }
    });
    
    // Interactive references
    $(".fs").on("touch click", function(){
        var fs = $(this);
        var figureName = fs.data("fig");
        var figure = $("#" + figureName);
        var targets = $(this).data("targets").split("|");
        var context = fs.parents(".figure-context");
        
        if (figure.hasClass("focused")) {
            if (fs.hasClass("active")) {
                context.find("figure").removeClass("focus");
                context.find("*").removeClass("focused");
                fs.removeClass("active");
            } else {
                context.find("*").removeClass("focus");
                for (var i = 0; i < targets.length; i++) {
                    figure.find("[data-name='" + targets[i] + "']").addClass("focus");
                }
                context.find(".fs").removeClass("active");
                fs.addClass("active");
            }
        } else {
            context.find("figure").addClass("focused");
            for (var i = 0; i < targets.length; i++) {
                figure.find("[data-name='" + targets[i] + "']").addClass("focus");
            }
            context.find(".fs").removeClass("active");
            fs.addClass("active");
        }
    });
    
    // Reset figure shapes
    $("figure").on("touch click", function(){
        var context = $(this).parents(".figure-context");
        context.find("figure").removeClass("focused");
        context.find(".fs").removeClass("active");
        context.find("*").removeClass("focus");
    });
    
    // SVGs
    $("svg").each(function(i){
        var svg = $(this);
        svg.wrap("<span class='svg'></span>");
        svg.attr("xmlns", "http://www.w3.org/2000/svg");
        svg.attr("preserveAspectRatio", "xMidYMid meet");
        svg.attr("role", "img");
        svg.attr("aria-labelledby", "svg" + i);
        svg.find("title").attr("id", "svg" + i);
    });
    
    // Prevent wrapping when oversized punctuation immediately follows a figure shape
    $(".fs").each(function(){
        var next = $(this)[0].nextSibling;
        if (next != null) {
            if (next.nodeType == 1 && ($(next).hasClass("os") || next.nodeName == "SUP")) {
                // Only wrap .fs + .os and not .fs + [text] + .os
                $(this).next(".os").addBack().wrapAll("<span class='nb'></span>");
            }
        }
    });
    
    // Copy figures into ternary nav
    $(".nav-ternary-grid a[data-figure]").each(function(){
        var link = $(this);
        var fig = $("#" + link.data("figure")).find("span").html();
        link.prepend("<span class='thumb'>" + fig + "</span>");
        link.find("text, figcaption").remove();
    });

    // Long s
    $(".latin").each(function() {
        var text = $(this).text();
        text = text.replace(/ss([a-eg-z])/g, "ſſ$1");
        text = text.replace(/s([a-eg-z])/g, "ſ$1");
        $(this).text(text);
    });
    $("#longs").on('click', function() {
      $(".latin").each(function() {
          var text = $(this).text();
          text = text.replace(/ſ/g, "s");
          $(this).text(text);
      });

    });
    
});
