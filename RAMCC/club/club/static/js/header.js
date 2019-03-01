let url = $(".events").attr("data-href");
$.ajax({
  url: url,
  method: "GET"
}).done((data) => {
  count = data.posts + data.forms;
  $(".btn__badge").append(count)
}).fail((e) => {
  console.log(e)
});
