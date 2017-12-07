/*
<%--
  Created by IntelliJ IDEA.
  User: apple
  Date: 06/11/2017
  Time: 8:56 PM
  To change this template use File | Settings | File Templates.
 --%>
 */

<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
  <head>
    <title>Hello World</title>
  </head>
  <body>
  <link href="https://s3.amazonaws.com/mturk-public/bs30/css/bootstrap.min.css" rel="stylesheet" />
  <section class="container" id="Other" style="margin-bottom:15px; padding: 10px 10px; font-family: Verdana, Geneva, sans-serif; color:#333333; font-size:0.9em;">
    <div class="row col-xs-12 col-md-12"><!-- Instructions -->
      <div class="panel panel-primary">
        <div class="panel-heading"><strong>Instructions</strong></div>

        <div class="panel-body">
          <p>Place a dot at specified location for each column and determine direction:</p>

          <ol>
            <li>1. Finding the head of the specimen. Move the mouse to the location.</li>
            <li>2. Annotate the location by clicking the left mouse. A small dot will appear at the location of the mouse. Please do not draw multiple dots on the image.</li>
            <li>- Annotation samples are given in the first row of images for each feature identification. All of the images for this task are the same specimen, but in different poses.</li> 
            <li>3. Repeat steps 1 and 2 for the tail of the specimen in the second column.</li> 
            <li>4. Select the Z direction of the specimen in column 3</li> 
            <li>- See examples of each direction option at: . Please take a look and use as reference</li> 
          </ol>
        </div>
      </div>
      <!-- End Instructions --><!-- Content Body -->

      <div style="display:none;">&nbsp;</div>
    </div>
  </section>
  <link href="https://ajax.googleapis.com/ajax/libs/jqueryui/1.10.3/themes/smoothness/jquery-ui.css" rel="stylesheet" /><script src="https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script><script src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.10.3/jquery-ui.js"></script>
  <div style="display:inline-block;vertical-align:top;">
    <h1>Draw a dot by clicking the mouse on the following area: ${objects_to_find}</h1>

    <p>Draw a dot using your mouse over each object that matches the search criteria &quot;${objects_to_find}&quot;. Then submit.</p>

    <%--<div id="bbox_annotator" style="display:inline-block">&nbsp;</div>--%>

    <div class="container">
      <table class="table">
        <thead>
        <tr>
          <th>#</th>
          <th>Head Position</th>
          <th>Tail Position</th>
          <th>Z Direction</th>
        </tr>
        </thead>
        <tbody>
        <% for (int i = 1; i <= 9; i++) { %>
        <tr>
          <th scope="row"><%= i %></th>
            <% if (i==1) { %>
              <td>
                <img alt="Placeholder" class="img-responsive" height="200" src="/Users/ktl014/Documents/ECE 191 Project/MTurk/SPC2-1441562601-021228-001-2316-2508-120-152.jpg" width="200" />
              </td>
              <td>
                <img alt="Placeholder" class="img-responsive" height="200" src="/Users/ktl014/Documents/ECE 191 Project/MTurk/SPC2-1441562601-021228-001-2316-2508-120-152.jpg" width="200" />
              </td>
            <% } else { %>
              <td>
                <img alt="Placeholder" class="img-responsive" height="200" src="/Users/ktl014/Documents/ECE 191 Project/MTurk/SPC2-1441562601-021228-001-2316-2508-120-152.jpg" width="200" />
              </td>
              <td>
                <img alt="Placeholder" class="img-responsive" height="200" src="/Users/ktl014/Documents/ECE 191 Project/MTurk/SPC2-1441562601-021228-001-2316-2508-120-152.jpg" width="200" />
              </td>
            <% } %>
            <form class="btn-group-vertical">
              <div class="radio"><label><input type="radio" name="specimen-radio-<%= i %>">Parallel</label></div>
              <div class="radio"><label><input type="radio" name="specimen-radio-<%= i %>">Facing Camera</label></div>
              <div class="radio"><label><input type="radio" name="specimen-radio-<%= i %>">Back to Camera</label></div>
              <div class="radio"><label><input type="radio" name="specimen-radio-<%= i %>">Out of Frame</label></div>
              <div class="radio"><label><input type="radio" name="specimen-radio-<%= i %>">Not Sure</label></div>
            </form>
          </td>
        </tr>
        <% } %>
        </tbody>
      </table>
    </div>

    <%--<div class="container">--%>
      <%--<div class="panel-group" id="accordion-group">--%>
        <%--<div class="panel panel-default" id="accordian">--%>
          <%--<div class="panel-heading">--%>
            <%--<h4 class="panel-title"><a data-parent="#accordion" data-toggle="collapse" href="#collapse1">Specimen 1</a></h4>--%>

            <%--<div class="panel-collapse collapse in" id="collapse1">--%>
              <%--<div class="row">--%>
                <%--<div class="col-sm-4">--%>
                  <%--<h3>Head</h3>--%>

                  <%--<div id="bbox_annotator-head" style="display:inline-block">&nbsp;</div>--%>
                  <%--<img alt="Placeholder" class="img-responsive" height="200" src="/Users/ktl014/Documents/ECE 191 Project/MTurk/SPC2-1441562601-021228-001-2316-2508-120-152.jpg" width="200" /></div>--%>

                <%--<div class="col-sm-4">--%>
                  <%--<h3>Tail</h3>--%>

                  <%--<div id="bbox_annotator-tail" style="display:inline-block">&nbsp;</div>--%>
                  <%--<img alt="Placeholder" class="img-responsive" height="200" src="/Users/ktl014/Documents/ECE 191 Project/MTurk/SPC2-1441562601-021228-001-2316-2508-120-152.jpg" width="200" /></div>--%>

                <%--<div class="col-sm-4">--%>
                  <%--<h3>Z Direction</h3>--%>
                  <%--<form class="btn-group-vertical">--%>
                    <%--<div class="radio"><label><input type="radio" name="specimen-radio-1">Parallel</label></div>--%>
                    <%--<div class="radio"><label><input type="radio" name="specimen-radio-1">Facing Camera</label></div>--%>
                    <%--<div class="radio"><label><input type="radio" name="specimen-radio-1">Back to Camera</label></div>--%>
                    <%--<div class="radio"><label><input type="radio" name="specimen-radio-1">Neither</label></div>--%>
                    <%--<div class="radio"><label><input type="radio" name="specimen-radio-1">Not Sure</label></div>--%>
                  <%--</form>--%>
                <%--</div>--%>
              <%--</div>--%>
            <%--</div>--%>
          <%--</div>--%>
        <%--</div>--%>
      <%--</div>--%>
    <%--</div>--%>

    <p>&nbsp;</p>

    <p>&nbsp;</p>

    <p id="button_paragraph"><input id="annotation_data" name="annotation_data" type="hidden" /> <input id="reset_button" type="reset" /></p>
  </div>
  <script type="text/javascript">
      (function() {
          var BBoxSelector;
          BBoxSelector = (function() {
              function BBoxSelector(image_frame, options) {
                  if (options == null) {
                      options = {};
                  }
                  options.input_method || (options.input_method = "text");
                  this.image_frame = image_frame;
                  this.border_width = options.border_width || 2;
                  this.selector = $('<div class="bbox_selector"></div>');
                  this.selector.css({
                      "border": this.border_width + "px dotted rgb(127,255,127)",
                      "position": "absolute"
                  });
                  this.image_frame.append(this.selector);
                  this.selector.css({
                      "border-width": this.border_width
                  });
                  this.selector.hide();
                  this.create_label_box(options);
              }
              BBoxSelector.prototype.create_label_box = function(options) {
                  var label, _i, _len, _ref;
                  options.labels || (options.labels = ["object"]);
                  this.label_box = $('<div class="label_box"></div>');
                  this.label_box.css({
                      "position": "absolute"
                  });
                  this.image_frame.append(this.label_box);
                  switch (options.input_method) {
                      case 'select':
                          if (typeof options.labels === "string") {
                              options.labels = [options.labels];
                          }
                          this.label_input = $('<select class="label_input" name="label"></select>');
                          this.label_box.append(this.label_input);
                          this.label_input.append($('<option value>choose an item</option>'));
                          _ref = options.labels;
                          for (_i = 0, _len = _ref.length; _i < _len; _i++) {
                              label = _ref[_i];
                              this.label_input.append('<option value="' + label + '">' + label + '</option>');
                          }
                          this.label_input.change(function(e) {
                              return this.blur();
                          });
                          break;
                      case 'text':
                          if (typeof options.labels === "string") {
                              options.labels = [options.labels];
                          }
                          this.label_input = $('<input class="label_input" name="label" ' + 'type="text" value>');
                          this.label_box.append(this.label_input);
                          this.label_input.autocomplete({
                              source: options.labels || [''],
                              autoFocus: true
                          });
                          break;
                      case 'fixed':
                          if ($.isArray(options.labels)) {
                              options.labels = options.labels[0];
                          }
                          this.label_input = $('<input class="label_input" name="label" type="text">');
                          this.label_box.append(this.label_input);
                          this.label_input.val(options.labels);
                          break;
                      default:
                          throw 'Invalid label_input parameter: ' + options.input_method;
                  }
                  return this.label_box.hide();
              };
              BBoxSelector.prototype.crop = function(pageX, pageY) {
                  var point;
                  return point = {
                      x: Math.min(Math.max(Math.round(pageX - this.image_frame.offset().left), 0), Math.round(this.image_frame.width() - 1)),
                      y: Math.min(Math.max(Math.round(pageY - this.image_frame.offset().top), 0), Math.round(this.image_frame.height() - 1))
                  };
              };
              BBoxSelector.prototype.start = function(pageX, pageY) {
                  this.pointer = this.crop(pageX, pageY);
                  this.offset = this.pointer;
                  this.refresh();
                  this.selector.show();
                  $('body').css('cursor', 'crosshair');
                  return document.onselectstart = function() {
                      return false;
                  };
              };
              BBoxSelector.prototype.update_rectangle = function(pageX, pageY) {
                  this.pointer = this.crop(pageX, pageY);
                  return this.refresh();
              };
              BBoxSelector.prototype.input_label = function(options) {
                  $('body').css('cursor', 'default');
                  document.onselectstart = function() {
                      return true;
                  };
                  this.label_box.show();
                  return this.label_input.focus();
              };
              BBoxSelector.prototype.finish = function(options) {
                  var data;
                  this.label_box.hide();
                  this.selector.hide();
                  data = this.rectangle();
                  data.label = $.trim(this.label_input.val().toLowerCase());
                  if (options.input_method !== 'fixed') {
                      this.label_input.val('');
                  }
                  return data;
              };
              BBoxSelector.prototype.rectangle = function() {
                  var rect, x1, x2, y1, y2;
                  x1 = Math.min(this.offset.x, this.pointer.x);
                  y1 = Math.min(this.offset.y, this.pointer.y);
                  x2 = Math.max(this.offset.x, this.pointer.x);
                  y2 = Math.max(this.offset.y, this.pointer.y);
                  return rect = {
                      left: x1,
                      top: y1,
                      width: x2 - x1 + 1,
                      height: y2 - y1 + 1
                  };
              };
              BBoxSelector.prototype.refresh = function() {
                  var rect;
                  rect = this.rectangle();
                  this.selector.css({
                      left: (rect.left - this.border_width) + 'px',
                      top: (rect.top - this.border_width) + 'px',
                      width: rect.width + 'px',
                      height: rect.height + 'px'
                  });
                  return this.label_box.css({
                      left: (rect.left - this.border_width) + 'px',
                      top: (rect.top + rect.height + this.border_width) + 'px'
                  });
              };
              BBoxSelector.prototype.get_input_element = function() {
                  return this.label_input;
              };
              return BBoxSelector;
          })();
          this.BBoxAnnotator = (function() {
              function BBoxAnnotator(options) {
                  var annotator, image_element;
                  annotator = this;
                  this.annotator_element = $(options.id || "#bbox_annotator");
                  this.border_width = options.border_width || 2;
                  this.show_label = options.show_label || (options.input_method !== "fixed");
                  this.image_frame = $('<div class="image_frame"></div>');
                  this.annotator_element.append(this.image_frame);
                  image_element = new Image();
                  image_element.src = options.url;
                  image_element.onload = function() {
                      options.width || (options.width = image_element.width);
                      options.height || (options.height = image_element.height);
                      annotator.annotator_element.css({
                          "width": (options.width + annotator.border_width * 2) + 'px',
                          "height": (options.height + annotator.border_width * 2) + 'px',
                          "cursor": "crosshair"
                      });
                      annotator.image_frame.css({
                          "background-image": "url('" + image_element.src + "')",
                          "width": options.width + "px",
                          "height": options.height + "px",
                          "position": "relative"
                      });
                      annotator.selector = new BBoxSelector(annotator.image_frame, options);
                      return annotator.initialize_events(annotator.selector, options);
                  };
                  image_element.onerror = function() {
                      return annotator.annotator_element.text("Invalid image URL: " + options.url);
                  };
                  this.entries = [];
                  this.onchange = options.onchange;
              }
              BBoxAnnotator.prototype.initialize_events = function(selector, options) {
                  var annotator, status;
                  status = 'free';
                  this.hit_menuitem = false;
                  annotator = this;
                  this.annotator_element.mousedown(function(e) {
                      if (!annotator.hit_menuitem) {
                          switch (status) {
                              case 'free':
                              case 'input':
                                  if (status === 'input') {
                                      selector.get_input_element().blur();
                                  }
                                  if (e.which === 1) {
                                      selector.start(e.pageX, e.pageY);
                                      status = 'hold';
                                  }
                          }
                      }
                      annotator.hit_menuitem = false;
                      return true;
                  });
                  $(window).mousemove(function(e) {
                      switch (status) {
                          case 'hold':
                              selector.update_rectangle(e.pageX, e.pageY);
                      }
                      return true;
                  });
                  $(window).mouseup(function(e) {
                      switch (status) {
                          case 'hold':
                              selector.update_rectangle(e.pageX, e.pageY);
                              selector.input_label(options);
                              status = 'input';
                              if (options.input_method === 'fixed') {
                                  selector.get_input_element().blur();
                              }
                      }
                      return true;
                  });
                  selector.get_input_element().blur(function(e) {
                      var data;
                      switch (status) {
                          case 'input':
                              data = selector.finish(options);
                              if (data.label) {
                                  annotator.add_entry(data);
                                  if (annotator.onchange) {
                                      annotator.onchange(annotator.entries);
                                  }
                              }
                              status = 'free';
                      }
                      return true;
                  });
                  selector.get_input_element().keypress(function(e) {
                      switch (status) {
                          case 'input':
                              if (e.which === 13) {
                                  selector.get_input_element().blur();
                              }
                      }
                      return e.which !== 13;
                  });
                  selector.get_input_element().mousedown(function(e) {
                      return annotator.hit_menuitem = true;
                  });
                  selector.get_input_element().mousemove(function(e) {
                      return annotator.hit_menuitem = true;
                  });
                  selector.get_input_element().mouseup(function(e) {
                      return annotator.hit_menuitem = true;
                  });
                  return selector.get_input_element().parent().mousedown(function(e) {
                      return annotator.hit_menuitem = true;
                  });
              };
              BBoxAnnotator.prototype.add_entry = function(entry) {
                  var annotator, box_element, close_button, text_box;
                  this.entries.push(entry);
                  box_element = $('<div class="annotated_bounding_box"></div>');
                  box_element.appendTo(this.image_frame).css({
                      "border": this.border_width + "px solid rgb(127,255,127)",
                      "position": "absolute",
                      "top": (entry.top - this.border_width) + "px",
                      "left": (entry.left - this.border_width) + "px",
                      "width": entry.width + "px",
                      "height": entry.height + "px",
                      "color": "rgb(127,255,127)",
                      "font-family": "monospace",
                      "font-size": "small"
                  });
                  close_button = $('<div></div>').appendTo(box_element).css({
                      "position": "absolute",
                      "top": "-8px",
                      "right": "-8px",
                      "width": "16px",
                      "height": "0",
                      "padding": "16px 0 0 0",
                      "overflow": "hidden",
                      "color": "#fff",
                      "background-color": "#030",
                      "border": "2px solid #fff",
                      "-moz-border-radius": "18px",
                      "-webkit-border-radius": "18px",
                      "border-radius": "18px",
                      "cursor": "pointer",
                      "-moz-user-select": "none",
                      "-webkit-user-select": "none",
                      "user-select": "none",
                      "text-align": "center"
                  });
                  $("<div></div>").appendTo(close_button).html('×').css({
                      "display": "block",
                      "text-align": "center",
                      "width": "16px",
                      "position": "absolute",
                      "top": "-2px",
                      "left": "0",
                      "font-size": "16px",
                      "line-height": "16px",
                      "font-family": '"Helvetica Neue", Consolas, Verdana, Tahoma, Calibri, ' + 'Helvetica, Menlo, "Droid Sans", sans-serif'
                  });
                  text_box = $('<div></div>').appendTo(box_element).css({
                      "overflow": "hidden"
                  });
                  if (this.show_label) {
                      text_box.text(entry.label);
                  }
                  annotator = this;
                  box_element.hover((function(e) {
                      return close_button.show();
                  }), (function(e) {
                      return close_button.hide();
                  }));
                  close_button.mousedown(function(e) {
                      return annotator.hit_menuitem = true;
                  });
                  close_button.click(function(e) {
                      var clicked_box, index;
                      clicked_box = close_button.parent(".annotated_bounding_box");
                      index = clicked_box.prevAll(".annotated_bounding_box").length;
                      clicked_box.detach();
                      annotator.entries.splice(index, 1);
                      return annotator.onchange(annotator.entries);
                  });
                  return close_button.hide();
              };
              BBoxAnnotator.prototype.clear_all = function(e) {
                  $(".annotated_bounding_box").detach();
                  this.entries.splice(0);
                  return this.onchange(this.entries);
              };
              return BBoxAnnotator;
          })();
      }).call(this);
      // Main entry point. Use a placeholder for image urls.
      $(document).ready(function() {
//          var assignment_id = turkGetParam('assignmentId', "");
          // Initialize the bounding-box annotator.
          var annotator = new BBoxAnnotator({
              url: "https://s3-us-west-1.amazonaws.com/planktonsummer17/ZP100/${image_url}",
              url: "http://turk.s3.amazonaws.com/stop_sign_picture.jpg",
              input_method: 'fixed', // Can be one of ['text', 'select', 'fixed']
              labels: ["Head","Tail"], // Label of the object.
              onchange: function(entries) {
                  $("#annotation_data").val(JSON.stringify(entries));
                  if (entries.length > 0 &&
                      assignment_id != "" &&
                      assignment_id != "ASSIGNMENT_ID_NOT_AVAILABLE") {
                      $("#submitButton").removeAttr("disabled");
                  }
                  else {
                      $("#submitButton").attr("disabled", "disabled");
                  }
              }
          });
          // Initialize the reset button.
          $("#reset_button").click(function(e) {
              annotator.clear_all();
          });
          // Disable the submission at the beginning.
          $("#submitButton").attr("disabled", "disabled");
          $("#submitButton").detach().appendTo("#button_paragraph");
          if (assignment_id == "ASSIGNMENT_ID_NOT_AVAILABLE") {
              $("#submitButton").val("This is preview");
          }
          console.log(assignment_id);
      });
  </script>
  </body>
</html>
