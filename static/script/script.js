$(document).ready(function () {
  let li = $(".black-sea-ul").find("li");
  let li1 = $(".direction-ul").find("li");
  $(li).click(function () {
    $(li).removeClass("active");
    $(this).addClass("active")
  })
  $(li1).click(function () {
    $(li1).removeClass("active");
    $(this).addClass("active")
  })
  $('.filter1-button').click(function () {
    $('.filter1-button').removeClass("active");
    $(this).addClass("active")
  })
  $(".burger-menu").click(function () {
    $(".header-menu nav").toggleClass("nav-responsive");
    $(this).find('span').toggleClass("backWhite")
    $(this).find('span').eq(0).toggleClass("rotate45");
    $(this).find('span').eq(1).toggle(100);
    $(this).find('span').eq(2).toggleClass("rotate-45");
    if ($(".logo-cont img").attr("src") === "img/logo.png") {
      $(".logo-cont img").attr("src", "img/footerLogo.png")
    } else {
      $(".logo-cont img").attr("src", "img/logo.png")
    }
  });
  $(".show-price-show").click(function () {
    $(this).closest(".card-body").find(".room-price").toggleClass('room-price-fixed hidden-none')
    $(this).find("i").toggleClass("flip")
  })

  function addSeparator(nStr) {
    nStr += '';
    var x = nStr.split('.');
    var x1 = x[0];
    var x2 = x.length > 1 ? '.' + x[1] : '';
    var rgx = /(\d+)(\d{3})/;
    while (rgx.test(x1)) {
      x1 = x1.replace(rgx, '$1' + '.' + '$2');
    }
    return x1 + x2;
  }

  function rangeInputChangeEventHandler(e) {
    var rangeGroup = $(this).attr('name'),
      minBtn = $(this).parent().children('.min'),
      maxBtn = $(this).parent().children('.max'),
      range_min = $(this).parent().find('.range_min'),
      range_max = $(this).parent().find('.range_max'),
      minVal = parseInt($(minBtn).val()),
      maxVal = parseInt($(maxBtn).val()),
      origin = $(this).className;
    if (origin === 'min' && minVal > maxVal - 5) {
      $(minBtn).val(maxVal - 5);
    }
    var minVal = parseInt($(minBtn).val());
    $(range_min).val(addSeparator(minVal * 100));
    if (origin === 'max' && maxVal - 5 < minVal) {
      $(maxBtn).val(5 + minVal);
    }
    var maxVal = parseInt($(maxBtn).val());
    $(range_max).val(addSeparator(maxVal * 100));
  }

  (function () {
    let range_min, range_max, minVal, maxVal;
    $(".range_min").val($(".min").val() * 100);
    $(".range_max").val($(".max").val() * 100);
    $('input[type="range"]').on('input', rangeInputChangeEventHandler);
  })();

  $(".tab-item").on("click", function () {
    $(".tab-item").removeClass('active')
    $(this).addClass('active');
  })

  function prevent(e) {
    e.preventDefault()
  }

  $(".filter1-button-cont").find("button").on("click", prevent)
  $(".showmore").on("click", function () {
    $(this).prev().toggleClass("ul-fixed-height")
    $(this).find('i').toggleClass("flip")
  });

  $(".showmore1").on("click", function () {
    $(this).prev().toggleClass("ul-fixed-height1")
    $(this).find('i').toggleClass("flip")
  });

  $(".showmore2").on("click", function () {
    $(this).prev().toggleClass("ul-fixed-height2")
    $(this).find('i').toggleClass("flip")
  });

  $(".dropbtn").on("click", function () {
    $(this).next().slideToggle()
  })

  $(".show-map").click(function () {
    let cloneVal = $(".curort-filter-map").clone()
    $(".modal-left").html(cloneVal)

    $(".range_min").val($(".min").val() * 1000);
    $(".range_max").val($(".max").val() * 1000);
    $('input[type="range"]').on('input', rangeInputChangeEventHandler);

    $('.filter1-button').click(function (e) {
      e.preventDefault()
      $('.filter1-button').removeClass("active");
      $(this).addClass("active")
    })
  });

  $(".show-filter").click(function () {
    $(".modal-filter").slideDown();
    let cloneVal = $(".curort-filter-map form").clone()
    $(".modal-filter").append(cloneVal)
    $(".range_min").val($(".min").val() * 1000);
    $(".range_max").val($(".max").val() * 1000);
    $('input[type="range"]').on('input', rangeInputChangeEventHandler);

    $('.filter1-button').click(function (e) {
      e.preventDefault()
      $('.filter1-button').removeClass("active");
      $(this).addClass("active")
    })
    $(".showmore").on("click", function () {
      $(this).prev().toggleClass("ul-fixed-height")
      $(this).find('i').toggleClass("flip")
    });

    $(".showmore1").on("click", function () {
      $(this).prev().toggleClass("ul-fixed-height1")
      $(this).find('i').toggleClass("flip")
    });

    $(".showmore2").on("click", function () {
      $(this).prev().toggleClass("ul-fixed-height2")
      $(this).find('i').toggleClass("flip")
    });
  })
  $(".show-little-map").click(function () {
    $(".modal-map").slideDown();
    let cloneVal = $(".modal-right").clone()
    $(".modal-map").append(cloneVal)
  })
  $(".closeModalFilter").click(function () {
    $(".modal-filter").slideUp();
  })
  $(".closeModalMap").click(function () {
    $(".modal-map").slideUp();
  })
  $(".add-object-form").find("button").not(".submit").on("click", function (e) {
    e.preventDefault()
  })
  $(".object-table-cont").find("table").find("tr").even().css("background", "#EDF4FF");
  $(".object-button-cont").find('li').click(function () {
    let dataScroll = $(this).attr("data-scroll")
    $('html,body').animate({
        scrollTop: $("." + dataScroll).offset().top
      },
      'slow');
  });
  $(".collaps-button").click(function () {
    $(this).toggleClass("flip");
    $(this).toggleClass("openDiv")
    $(this).parents(".faq").toggleClass("fixed-faq")
  })
  $(".room-rent-head").find('li').click(function () {
    if ($(this).attr('data-class') === "addObjectli") {
      $(".addObject").slideDown()
      $(".orderCall").slideUp()
    } else {
      $(".orderCall").slideDown()
      $(".addObject").slideUp()
    }
  })
  $(".addOptionsUl").find("input[type='checkbox']").click(function () {
    let attribute = $(this).attr("id");
    $("div[data-show='" + attribute + "']").toggle();
  })
  $(".main-ul").find("li").click(function () {
    let attribute = $(this).attr("data-show");
    changeMainTab(attribute)
  })
  $(".direction-ul").find("li").click(function () {
    let attribute = $(this).attr("data-show");
    changeMainTab1(attribute, this)
  })


  $(".black-sea-ul").find("li").click(function () {
    let attribute = $(this).attr("data-show");
    changeMainTab1(attribute, this)
  })
  if (window.location.hash) {
    id = window.location.hash.split("-")[1];
    changeMainTab(id)
  }

  function changeMainTab(attribute) {
    $(".main-tab-content").find('div.tabContent').removeClass('active')
    $("#" + attribute + "").addClass("active");
    $("#" + attribute + "").toggle();
    $(".main-ul").find("li").removeClass("active");
    $(".main-ul").find("li[data-show='" + attribute + "'").addClass("active");
    window.location.hash = "tab-" + attribute;
  }

  function changeMainTab1(attribute, thisval) {
    $(thisval).closest("ul").next(".direction-tab-content").find('div.tabContent').removeClass('active')
    $("#" + attribute + "").addClass("active");
    $("#" + attribute + "").toggle();
    $(thisval).closest("ul").find("li").removeClass("active");
    $(thisval).closest("ul").find("li[data-show='" + attribute + "'").addClass("active");
  }


  $(".imgLoad").change(function () {
    if (this.files && this.files[0]) {
      var reader = new FileReader();
      let thisImg = this
      reader.onload = function (e) {
        $(thisImg).closest(".image-loaded").find('.loadedImage').attr('src', e.target.result);
        $(thisImg).closest(".image-loaded").find('.loadedImage').css("height", "100%");
        $(thisImg).closest(".image-loaded").find('.closeButton').css("display", "flex");
      }
      reader.readAsDataURL(this.files[0]);
    }
  });
  $(".closeButton").on("click", function () {
    $(this).closest(".image-loaded").find('.loadedImage').css("height", "0");
    $(this).css("display", "none");
  })
  let num = 0
  $(".addPeriud").click(function (e) {
    e.preventDefault()
    $(".hidden-periuds").find(".hidden-periud").eq(num).removeClass('d-none')
    num++
  })
  $(".toggleContButton").click(function () {
    $(".toggleCont").slideUp()
    $(".ready-number").removeClass("d-none")
  })
  $(".editDescription").click(function () {
    $(this).parents(".descriptionTabOptionsHead").slideUp()
    $(this).parents(".descriptionTabOptionsHead").next(".secondDiv").slideDown()
  })
  $(".dropdown").find("a").click(function (e) {
    e.preventDefault()
    let thisVar = $(this).text()
    $(this).parents(".dropdown").find(".dropbtn ").find("span").html(thisVar)
    $(this).parent(".dropdown-content").slideUp()
  })


  let count = 0
  let arr = []
  $(".newObject").click(function () {
    if (count == 12) {
      return false
    } else {
      count++

    }
  })
  $(".hidden-periuds").find("input").on("change", function () {
    arr.push(this)
  })

  $(".hidden-periuds").find(".delete-card").on("click", function () {
    $(this).closest(".hidden-periud").remove()
    count--
  })


  $(".toggleContButton").click(function () {
    for (let i = 0; i < count; i++) {
      for (let j = 0; j < 2; j++) {
        $($(".loop-table")[j]).find("tr").eq(0).append(
          `<td class="ready-number-cont-date"><div><span class="input-${i + 1}"></span> <span class="span-devider">  </span> <span class="input-${i + 1}-1"></span></div></td>`
        )
        $($(".loop-table")[j]).find("tr").eq(1).append(
          `<td><input type="text" placeholder="За номер (руб)"></td>`
        )
        $($(".loop-table")[j]).find("tr").eq(2).append(
          `<td><input type="text" placeholder="За номер (руб)"></td>`
        )
      }
    }
    for (let i = 0; i < arr.length; i++) {
      $("." + arr[i].id).html($("#" + arr[i].id).val())
      $("." + arr[i].id).next(".span-devider").html(" - ")
    }
  })

  Dropzone.autoDiscover=false;
  const myDropzone= new Dropzone('#my-dropzone',{

    maxFiles:5,
    maxFilesize:2,
    acceptedFiles:'.jpg',
})

})

$(window).on('scroll', function() {

	if($(window).scrollTop() > 90) {
		$('#object').addClass('fixed-menu')
		$('.object-section').addClass('fixed-menu')
	} else {
		$('#object').removeClass('fixed-menu')
		$('.object-section').removeClass('fixed-menu')
	}

});

if($(window).width() > 768) {

	let containerHeght = $('.row').height(),
			containerDistance = $('.row').offset().top,
			containerSum = containerDistance + containerHeght;

	$(window).on('scroll', function() {

		let distance = document.querySelector(".object-right").getBoundingClientRect();

		if(distance.top > 90 || distance.top < 0) {
			$('.object-right').addClass('fixed')
		}

		if( ($(window).scrollTop() < 240)) {
			$('.object-right').removeClass('fixed')
		}

		if($(window).scrollTop() > (containerSum - 114)) {
			$('.object-right').addClass('absolute')
		} else {
			$('.object-right').removeClass('absolute')
		}

	});

}

//Table
$('.object-table-cont tr').each(function(i, item) {
	if (i % 2 === 0) {
		$(item).find(':first-child').addClass('sticky').addClass('even')
	} else {
		$(item).find(':first-child').addClass('sticky').addClass('odd')
	}

});
