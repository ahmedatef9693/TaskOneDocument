// Copyright (c) 2023, ahmed and contributors
// For license information, please see license.txt

var csv_xlsx = false;
var number_of_sheets = -1;
var listofoptions = [];
frappe.ui.form.on("Task One Document", {
  refresh: function (frm) {},
  onload: function (frm) {
    set_field_options("sheet_no", listofoptions);
    // frm.set_df_property("file_value", "reqd", 1);
    // vip
    // document.getElementsByClassName("btn btn-xs btn-default")[1]
  },
  generate: (frm) => {
    var file_extension_check_csv = frm.doc.file_value
      .toString()
      .indexOf(".csv");
    var file_extension_check_xlsx = frm.doc.file_value
      .toString()
      .indexOf(".xlsx");

    var checkPrivateFile = frm.doc.file_value.toString().indexOf("/private");
    var file_folder = "";
    if (checkPrivateFile === -1) {
      file_folder = "/public";
    }

    if (file_extension_check_csv !== -1 || file_extension_check_xlsx !== -1) {
      if (file_extension_check_csv !== -1) {
        frm
          .call("send_file", {
            csv_file_path: file_folder + frm.doc.file_value,
          })
          .then((data) => {
            // var newData = JSON.parse(data.message);
            // var text_area = $(".input-with-feedback")[0];
            // for (const k in newData) {
            //   // console.log(k + `${newData[k]}`);
            //   text_area.value += `${k} : ${newData[k]}\n`;
            // }
          });
        csv_xlsx = true;
      } else if (file_extension_check_xlsx !== -1) {
        // frm.set_df_property("sheet_no", "read_only", 0);
        var myForm = frm;
        frm
          .call("send_xlsx_file", {
            xlsx_file_path: file_folder + frm.doc.file_value,
          })
          .then((numberofsheets) => {
            console.log(numberofsheets);
            number_of_sheets = Number(numberofsheets.message);
            frappe.msgprint(
              "number of sheets = " + numberofsheets.message.toString()
            );

            for (let index = 0; index < number_of_sheets; index++) {
              listofoptions[index] = index + 1;
            }
            console.log(listofoptions);
          });
        csv_xlsx = true;
      }
    } else {
      frm.set_value("dictionary", "");
      frm.set_value("gender", "");
      frm.set_value("sheet_no", "");
      csv_xlsx = false;
      // frappe.msgprint("csv_xlsx value : " + csv_xlsx);
      frappe.throw("Error App Accept Only csv and xlsx extension");
    }
  },
  clear_dict: (frm) => {
    frm.call("clear_data", {}).then((data) => {});
    // frm.set_value("dictionary", " ");
    // frappe.msgprint("cleared");
  },
});

frappe.ui.form.on("Task One Document", "gender", function (frm) {
  // frappe.msgprint("csv_xlsx value : " + csv_xlsx);
  if (csv_xlsx && frm.doc.file_value) {
    if (frm.doc.gender == "Male") {
      // frm.set_value("gender", "Male");
      frm
        .call("filter_data", {
          gender_type: "Male",
        })
        .then((data) => {});
    } else if (frm.doc.gender == "Female") {
      // frm.set_value("gender", "Female");
      frm
        .call("filter_data", {
          gender_type: "Female",
        })
        .then((data) => {});
    } else {
      frm
        .call("filter_data", {
          gender_type: "",
        })
        .then((data) => {});
    }
  } else {
    frappe.throw("cannot change gender please check format");
  }
});

frappe.ui.form.on("Task One Document", "sheet_no", function (frm) {
  var my_form = frm;
  if (my_form.doc.file_value.toString().indexOf(".csv") !== -1) {
    frappe.throw("csv file has no sheets");
  } else if (my_form.doc.file_value.toString().indexOf(".xlsx") !== -1) {
    frappe.msgprint("selected sheet = " + my_form.doc.sheet_no);
    frm
      .call("display_sheet", {
        current_sheet: my_form.doc.sheet_no,
      })
      .then((data) => {
        // my_form.set_value("sheet_no", my_form.doc.sheet_no);
      });
  } else {
    frappe.msgprint("cannot change sheets number please check format");
  }
});
