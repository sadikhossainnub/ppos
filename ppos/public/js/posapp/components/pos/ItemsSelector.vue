<template>
  <div class="h-100 d-flex flex-column">
    <div class="px-6 py-4 bg-white">
      <v-row align="center" no-gutters>
        <v-col cols="4">
          <h2 class="text-h5 font-weight-bold text-grey-darken-3">All Items</h2>
        </v-col>
        <v-col cols="4" class="px-2">
          <v-text-field
            v-model="debounce_search"
            placeholder="Search item code, serial or barcode..."
            prepend-inner-icon="mdi-magnify"
            flat
            density="compact"
            variant="solo-filled"
            bg-color="grey-lighten-4"
            rounded="lg"
            hide-details
          ></v-text-field>
        </v-col>
        <v-col cols="4">
          <v-select
            v-model="item_group"
            :items="items_group"
            placeholder="Category"
            flat
            density="compact"
            variant="solo-filled"
            bg-color="grey-lighten-4"
            rounded="lg"
            hide-details
            @update:model-value="search_onchange"
          ></v-select>
        </v-col>
      </v-row>
    </div>

    <v-divider></v-divider>

    <div class="flex-grow-1 overflow-y-auto px-4 py-4 bg-white">
      <v-progress-linear
        v-if="loading"
        indeterminate
        color="primary"
        height="2"
      ></v-progress-linear>

      <div v-if="items_view == 'card'">
        <v-row dense>
          <v-col
            v-for="(item, idx) in filtred_items"
            :key="idx"
            xl="3"
            lg="4"
            md="6"
            sm="6"
            cols="6"
            class="pa-2"
          >
            <v-card 
              hover 
              @click="add_item(item)" 
              class="item-card border rounded-xl"
              elevation="0"
            >
              <div class="pa-3 position-relative">
                <div class="badge-container position-absolute" style="top: 10px; right: 10px; z-index: 1;">
                  <v-chip
                    size="x-small"
                    :color="item.actual_qty > 0 ? 'success' : 'error'"
                    variant="flat"
                    density="comfortable"
                    class="font-weight-bold"
                  >
                    <v-icon start size="10" icon="mdi-circle"></v-icon>
                    {{ formtFloat(item.actual_qty) }}
                  </v-chip>
                </div>
                
                <v-img
                  :src="item.image || '/assets/ppos/js/posapp/components/pos/placeholder-image.png'"
                  height="140px"
                  cover
                  class="rounded-lg bg-grey-lighten-4 mb-3"
                >
                  <template v-slot:placeholder>
                    <div class="fill-height d-flex align-center justify-center text-h3 font-weight-bold text-grey-lighten-1">
                      {{ item.item_name.substring(0, 2).toUpperCase() }}
                    </div>
                  </template>
                </v-img>
                
                <div class="text-subtitle-1 font-weight-bold text-truncate mb-1">{{ item.item_name }}</div>
                <div class="text-body-2 font-weight-bold text-primary">
                  {{ currencySymbol(item.currency || pos_profile.currency) }} {{ formtCurrency(item.rate || item.price_list_rate) }} 
                  <span class="text-caption text-grey font-weight-regular">/ {{ item.stock_uom }}</span>
                </div>
              </div>
            </v-card>
          </v-col>
        </v-row>
      </div>

      <div v-else-if="items_view == 'list'">
        <v-data-table
          :headers="getItmesHeaders()"
          :items="filtred_items"
          item-value="item_code"
          density="comfortable"
          hover
        >
          <template v-slot:bottom></template>
          <template v-slot:item="{ item }">
            <tr @click="add_item(item)" style="cursor: pointer">
              <td class="font-weight-bold">{{ item.item_name }}</td>
              <td v-if="pos_profile.ppos_display_item_code" class="text-grey">{{ item.item_code }}</td>
              <td class="text-primary font-weight-bold">
                {{ currencySymbol(item.currency || pos_profile.currency) }} {{ formtCurrency(item.rate || item.price_list_rate) }}
              </td>
              <td>
                <v-chip size="small" :color="item.actual_qty > 0 ? 'success' : 'error'" variant="tonal">
                  {{ formtFloat(item.actual_qty) }} {{ item.stock_uom }}
                </v-chip>
              </td>
            </tr>
          </template>
        </v-data-table>
      </div>
    </div>
    
    <div class="pa-4 bg-white border-t d-flex align-center">
      <v-btn-toggle
        v-model="items_view"
        color="primary"
        variant="tonal"
        density="compact"
        mandatory
        rounded="lg"
      >
        <v-btn value="list" prepend-icon="mdi-format-list-bulleted">List</v-btn>
        <v-btn value="card" prepend-icon="mdi-view-grid">Grid</v-btn>
      </v-btn-toggle>
      
      <v-spacer></v-spacer>
      
      <v-btn
        variant="text"
        color="primary"
        prepend-icon="mdi-ticket-percent"
        @click="show_coupons"
        class="mr-2"
      >
        {{ couponsCount }} Coupons
      </v-btn>
      <v-btn
        variant="tonal"
        color="primary"
        prepend-icon="mdi-sale"
        @click="show_offers"
      >
        {{ offersCount }} Offers ({{ appliedOffersCount }} Applied)
      </v-btn>
    </div>
  </div>
</template>

<style scoped>
.item-card {
  transition: transform 0.2s;
  border-radius: 12px !important;
}
.item-card:hover {
  transform: translateY(-4px);
  border-color: #1A1A1A !important;
}
</style>

<script>
import { evntBus } from "../../bus";
import format from "../../format";
import _ from "lodash";

export default {
  mixins: [format],
  data: () => ({
    pos_profile: "",
    flags: {},
    items_view: "list",
    item_group: "ALL",
    loading: false,
    items_group: ["ALL"],
    items: [],
    search: "",
    first_search: "",
    itemsPerPage: 1000,
    offersCount: 0,
    appliedOffersCount: 0,
    couponsCount: 0,
    appliedCouponsCount: 0,
    customer_price_list: null,
    customer: null,
    new_line: false,
    qty: 1,
  }),

  watch: {
    filtred_items(new_value, old_value) {
      if (!this.pos_profile.pose_use_limit_search) {
        if (new_value.length != old_value.length) {
          this.update_items_details(new_value);
        }
      }
    },
    customer() {
      this.get_items();
    },
    new_line() {
      evntBus.emit("set_new_line", this.new_line);
    },
  },

  methods: {
    show_offers() {
      evntBus.emit("show_offers", "true");
    },
    show_coupons() {
      evntBus.emit("show_coupons", "true");
    },
    get_items() {
      if (!this.pos_profile) {
        console.error("No POS Profile");
        return;
      }
      const vm = this;
      this.loading = true;
      let search = this.get_search(this.first_search);
      let gr = "";
      let sr = "";
      if (search) {
        sr = search;
      }
      if (vm.item_group != "ALL") {
        gr = vm.item_group.toLowerCase();
      }
      if (
        vm.pos_profile.ppos_local_storage &&
        localStorage.items_storage &&
        !vm.pos_profile.pose_use_limit_search
      ) {
        vm.items = JSON.parse(localStorage.getItem("items_storage"));
        evntBus.emit("set_all_items", vm.items);
        vm.loading = false;
      }
      frappe.call({
        method: "ppos.ppos.api.posapp.get_items",
        args: {
          pos_profile: vm.pos_profile,
          price_list: vm.customer_price_list,
          item_group: gr,
          search_value: sr,
          customer: vm.customer,
        },
        callback: function (r) {
          if (r.message) {
            vm.items = r.message;
            evntBus.emit("set_all_items", vm.items);
            vm.loading = false;
            console.info("Items Loaded");
            if (
              vm.pos_profile.ppos_local_storage &&
              !vm.pos_profile.pose_use_limit_search
            ) {
              localStorage.setItem("items_storage", "");
              try {
                localStorage.setItem(
                  "items_storage",
                  JSON.stringify(r.message)
                );
              } catch (e) {
                console.error(e);
              }
            }
            if (vm.pos_profile.pose_use_limit_search) {
              vm.enter_event();
            }
          }
        },
      });
    },
    get_items_groups() {
      if (!this.pos_profile) {
        console.log("No POS Profile");
        return;
      }
      if (this.pos_profile.item_groups.length > 0) {
        this.pos_profile.item_groups.forEach((element) => {
          if (element.item_group !== "All Item Groups") {
            this.items_group.push(element.item_group);
          }
        });
      } else {
        const vm = this;
        frappe.call({
          method: "ppos.ppos.api.posapp.get_items_groups",
          args: {},
          callback: function (r) {
            if (r.message) {
              r.message.forEach((element) => {
                vm.items_group.push(element.name);
              });
            }
          },
        });
      }
    },
    getItmesHeaders() {
      const items_headers = [
        {
          title: __("Name"),
          align: "start",
          sortable: true,
          key: "item_name",
        },
        {
          title: __("Code"),
          align: "start",
          sortable: true,
          key: "item_code",
        },
        { title: __("Rate"), key: "rate", align: "start" },
        { title: __("Available QTY"), key: "actual_qty", align: "start" },
        { title: __("UOM"), key: "stock_uom", align: "start" },
      ];
      if (!this.pos_profile.ppos_display_item_code) {
        items_headers.splice(1, 1);
      }

      return items_headers;
    },
    add_item(item) {
      if (item.raw) item = item.raw; // In case it's passed from a row click
      item = { ...item };
      if (item.has_variants) {
        evntBus.emit("open_variants_model", { item, items: this.items });
      } else {
        if (!item.qty || item.qty === 1) {
          item.qty = Math.abs(this.qty);
        }
        evntBus.emit("add_item", item);
        this.qty = 1;
      }
    },
    enter_event() {
      let match = false;
      if (!this.filtred_items.length || !this.first_search) {
        return;
      }
      const qty = this.get_item_qty(this.first_search);
      const new_item = { ...this.filtred_items[0] };
      new_item.qty = flt(qty);
      new_item.item_barcode.forEach((element) => {
        if (this.search == element.barcode) {
          new_item.uom = element.ppos_uom;
          match = true;
        }
      });
      if (
        !new_item.to_set_serial_no &&
        new_item.has_serial_no &&
        this.pos_profile.ppos_search_serial_no
      ) {
        new_item.serial_no_data.forEach((element) => {
          if (this.search && element.serial_no == this.search) {
            new_item.to_set_serial_no = this.first_search;
            match = true;
          }
        });
      }
      if (this.flags.serial_no) {
        new_item.to_set_serial_no = this.flags.serial_no;
      }
      if (
        !new_item.to_set_batch_no &&
        new_item.has_batch_no &&
        this.pos_profile.ppos_search_batch_no
      ) {
        new_item.batch_no_data.forEach((element) => {
          if (this.search && element.batch_no == this.search) {
            new_item.to_set_batch_no = this.first_search;
            new_item.batch_no = this.first_search;
            match = true;
          }
        });
      }
      if (this.flags.batch_no) {
        new_item.to_set_batch_no = this.flags.batch_no;
      }
      if (match) {
        this.add_item(new_item);
        this.search = null;
        this.first_search = null;
        this.debounce_search = null;
        this.flags.serial_no = null;
        this.flags.batch_no = null;
        this.qty = 1;
        if (this.$refs.debounce_search) {
          this.$refs.debounce_search.focus();
        }
      }
    },
    search_onchange() {
      const vm = this;
      if (vm.pos_profile.pose_use_limit_search) {
        vm.get_items();
      } else {
        vm.enter_event();
      }
    },
    get_item_qty(first_search) {
      let scal_qty = Math.abs(this.qty);
      if (first_search.startsWith(this.pos_profile.ppos_scale_barcode_start)) {
        let pesokg1 = first_search.substr(7, 5);
        let pesokg;
        if (pesokg1.startsWith("0000")) {
          pesokg = "0.00" + pesokg1.substr(4);
        } else if (pesokg1.startsWith("000")) {
          pesokg = "0.0" + pesokg1.substr(3);
        } else if (pesokg1.startsWith("00")) {
          pesokg = "0." + pesokg1.substr(2);
        } else if (pesokg1.startsWith("0")) {
          pesokg =
            pesokg1.substr(1, 1) + "." + pesokg1.substr(2, pesokg1.length);
        } else if (!pesokg1.startsWith("0")) {
          pesokg =
            pesokg1.substr(0, 2) + "." + pesokg1.substr(2, pesokg1.length);
        }
        scal_qty = pesokg;
      }
      return scal_qty;
    },
    get_search(first_search) {
      let search_term = "";
      if (
        first_search &&
        first_search.startsWith(this.pos_profile.ppos_scale_barcode_start)
      ) {
        search_term = first_search.substr(0, 7);
      } else {
        search_term = first_search;
      }
      return search_term;
    },
    esc_event() {
      this.search = null;
      this.first_search = null;
      this.qty = 1;
      if (this.$refs.debounce_search) {
        this.$refs.debounce_search.focus();
      }
    },
    update_items_details(items) {
      const vm = this;
      frappe.call({
        method: "ppos.ppos.api.posapp.get_items_details",
        args: {
          pos_profile: vm.pos_profile,
          items_data: items,
        },
        callback: function (r) {
          if (r.message) {
            items.forEach((item) => {
              const updated_item = r.message.find(
                (element) => element.item_code == item.item_code
              );
              if (updated_item) {
                item.actual_qty = updated_item.actual_qty;
                item.serial_no_data = updated_item.serial_no_data;
                item.batch_no_data = updated_item.batch_no_data;
                item.item_uoms = updated_item.item_uoms;
              }
            });
          }
        },
      });
    },
    update_cur_items_details() {
      this.update_items_details(this.filtred_items);
    },
    scan_barcoud() {
      const vm = this;
      if (window.onScan) {
        onScan.attachTo(document, {
          suffixKeyCodes: [],
          keyCodeMapper: function (oEvent) {
            oEvent.stopImmediatePropagation();
            return onScan.decodeKeyEvent(oEvent);
          },
          onScan: function (sCode) {
            setTimeout(() => {
              vm.trigger_onscan(sCode);
            }, 300);
          },
        });
      }
    },
    trigger_onscan(sCode) {
      if (this.filtred_items.length == 0) {
        evntBus.emit("show_mesage", {
          text: `No Item has this barcode "${sCode}"`,
          color: "error",
        });
        frappe.utils.play_sound("error");
      } else {
        this.enter_event();
        this.debounce_search = null;
        this.search = null;
      }
    },
    generateWordCombinations(inputString) {
      const words = inputString.split(" ");
      const combinations = [];

      function permute(arr, m = []) {
        if (arr.length === 0) {
          combinations.push(m.join(" "));
        } else {
          for (let i = 0; i < arr.length; i++) {
            const current = arr.slice();
            const next = current.splice(i, 1);
            permute(current.slice(), m.concat(next));
          }
        }
      }

      permute(words);

      return combinations;
    },
  },

  computed: {
    filtred_items() {
      this.search = this.get_search(this.first_search);
      if (!this.pos_profile.pose_use_limit_search) {
        let filtred_list = [];
        let filtred_group_list = [];
        if (this.item_group != "ALL") {
          filtred_group_list = this.items.filter((item) =>
            item.item_group
              .toLowerCase()
              .includes(this.item_group.toLowerCase())
          );
        } else {
          filtred_group_list = this.items;
        }
        if (!this.search || this.search.length < 3) {
          if (
            this.pos_profile.ppos_show_template_items &&
            this.pos_profile.ppos_hide_variants_items
          ) {
            return (filtred_list = filtred_group_list
              .filter((item) => !item.variant_of)
              .slice(0, 50));
          } else {
            return (filtred_list = filtred_group_list.slice(0, 50));
          }
        } else if (this.search) {
          filtred_list = filtred_group_list.filter((item) => {
            let found = false;
            for (let element of item.item_barcode) {
              if (element.barcode == this.search) {
                found = true;
                break;
              }
            }
            return found;
          });
          if (filtred_list.length == 0) {
            filtred_list = filtred_group_list.filter((item) =>
              item.item_code.toLowerCase().includes(this.search.toLowerCase())
            );
            if (filtred_list.length == 0) {
              const search_combinations = this.generateWordCombinations(
                this.search
              );
              filtred_list = filtred_group_list.filter((item) => {
                let found = false;
                for (let element of search_combinations) {
                  element = element.toLowerCase().trim();
                  let element_regex = new RegExp(
                    `.*${element.split("").join(".*")}.*`
                  );
                  if (element_regex.test(item.item_name.toLowerCase())) {
                    found = true;
                    break;
                  }
                }
                return found;
              });
            }
            if (
              filtred_list.length == 0 &&
              this.pos_profile.ppos_search_serial_no
            ) {
              filtred_list = filtred_group_list.filter((item) => {
                let found = false;
                for (let element of item.serial_no_data) {
                  if (element.serial_no == this.search) {
                    found = true;
                    this.flags.serial_no = this.search;
                    break;
                  }
                }
                return found;
              });
            }
            if (
              filtred_list.length == 0 &&
              this.pos_profile.ppos_search_batch_no
            ) {
              filtred_list = filtred_group_list.filter((item) => {
                let found = false;
                for (let element of item.batch_no_data) {
                  if (element.batch_no == this.search) {
                    found = true;
                    this.flags.batch_no = this.search;
                    break;
                  }
                }
                return found;
              });
            }
          }
        }
        if (
          this.pos_profile.ppos_show_template_items &&
          this.pos_profile.ppos_hide_variants_items
        ) {
          return filtred_list.filter((item) => !item.variant_of).slice(0, 50);
        } else {
          return filtred_list.slice(0, 50);
        }
      } else {
        return this.items.slice(0, 50);
      }
    },
    debounce_search: {
      get() {
        return this.first_search;
      },
      set: _.debounce(function (newValue) {
        this.first_search = newValue;
      }, 200),
    },
  },

  created() {
    evntBus.on("register_pos_profile", (data) => {
      this.pos_profile = data.pos_profile;
      this.get_items();
      this.get_items_groups();
      this.items_view = this.pos_profile.ppos_default_card_view
        ? "card"
        : "list";
    });
    evntBus.on("update_cur_items_details", () => {
      this.update_cur_items_details();
    });
    evntBus.on("update_offers_counters", (data) => {
      this.offersCount = data.offersCount;
      this.appliedOffersCount = data.appliedOffersCount;
    });
    evntBus.on("update_coupons_counters", (data) => {
      this.couponsCount = data.couponsCount;
      this.appliedCouponsCount = data.appliedCouponsCount;
    });
    evntBus.on("update_customer_price_list", (data) => {
      this.customer_price_list = data;
    });
    evntBus.on("update_customer", (data) => {
      this.customer = data;
    });
  },

  mounted() {
    this.scan_barcoud();
  },
};
</script>

<style scoped></style>
