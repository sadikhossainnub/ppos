<template>
  <div>
    <v-card v-if="customer" class="pa-4 mb-4 rounded-xl border-dashed" border>
      <div class="d-flex align-center">
        <v-avatar color="grey-lighten-4" size="56" class="mr-4">
          <span class="text-h6 font-weight-bold text-grey-darken-1">{{ customer.substring(0, 1).toUpperCase() }}</span>
        </v-avatar>
        <div class="flex-grow-1">
          <div class="text-subtitle-1 font-weight-bold">{{ customer }}</div>
          <div class="text-caption text-grey">Walking Customer / Balance: 0</div>
        </div>
        <v-btn icon="mdi-close" variant="text" size="small" @click="customer = null"></v-btn>
      </div>
    </v-card>

    <v-autocomplete
      v-else
      clearable
      auto-select-first
      color="primary"
      placeholder="Search or add customer..."
      v-model="customer"
      :items="customers"
      item-title="customer_name"
      item-value="name"
      variant="solo-filled"
      bg-color="grey-lighten-4"
      flat
      rounded="lg"
      :no-data-text="__('Customer not found')"
      hide-details
      :custom-filter="customFilter"
      :disabled="readonly"
      prepend-inner-icon="mdi-account-search"
      append-inner-icon="mdi-plus"
      @click:append-inner="new_customer"
    >
      <template v-slot:item="{ props, item }">
        <v-list-item v-bind="props">
          <v-list-item-title class="font-weight-bold">
            {{ item.raw.customer_name }}
          </v-list-item-title>
          <v-list-item-subtitle class="text-caption">
            ID: {{ item.raw.name }}
          </v-list-item-subtitle>
        </v-list-item>
      </template>
    </v-autocomplete>
    
    <UpdateCustomer></UpdateCustomer>
  </div>
</template>

<script>
import { evntBus } from '../../bus';
import UpdateCustomer from './UpdateCustomer.vue';
export default {
  data: () => ({
    pos_profile: '',
    customers: [],
    customer: '',
    readonly: false,
    customer_info: {},
  }),

  components: {
    UpdateCustomer,
  },

  methods: {
    get_customer_names() {
      const vm = this;
      if (this.customers.length > 0) {
        return;
      }
      if (vm.pos_profile.ppos_local_storage && localStorage.customer_storage) {
        vm.customers = JSON.parse(localStorage.getItem('customer_storage'));
      }
      frappe.call({
        method: 'ppos.ppos.api.posapp.get_customer_names',
        args: {
          pos_profile: this.pos_profile.pos_profile,
        },
        callback: function (r) {
          if (r.message) {
            vm.customers = r.message;
            console.info('loadCustomers');
            if (vm.pos_profile.ppos_local_storage) {
              localStorage.setItem('customer_storage', '');
              localStorage.setItem(
                'customer_storage',
                JSON.stringify(r.message)
              );
            }
          }
        },
      });
    },
    new_customer() {
      evntBus.emit('open_update_customer', null);
    },
    edit_customer() {
      evntBus.emit('open_update_customer', this.customer_info);
    },
    customFilter(itemTitle, queryText, item) {
      const textOne = item.raw.customer_name
        ? item.raw.customer_name.toLowerCase()
        : '';
      const textTwo = item.raw.tax_id ? item.raw.tax_id.toLowerCase() : '';
      const textThree = item.raw.email_id ? item.raw.email_id.toLowerCase() : '';
      const textFour = item.raw.mobile_no ? item.raw.mobile_no.toLowerCase() : '';
      const textFifth = item.raw.name.toLowerCase();
      const searchText = queryText.toLowerCase();

      return (
        textOne.indexOf(searchText) > -1 ||
        textTwo.indexOf(searchText) > -1 ||
        textThree.indexOf(searchText) > -1 ||
        textFour.indexOf(searchText) > -1 ||
        textFifth.indexOf(searchText) > -1
      );
    },
  },

  created() {
    this.$nextTick(function () {
      evntBus.on('register_pos_profile', (pos_profile) => {
        this.pos_profile = pos_profile;
        this.get_customer_names();
      });
      evntBus.on('payments_register_pos_profile', (pos_profile) => {
        this.pos_profile = pos_profile;
        this.get_customer_names();
      });
      evntBus.on('set_customer', (customer) => {
        this.customer = customer;
      });
      evntBus.on('add_customer_to_list', (customer) => {
        this.customers.push(customer);
      });
      evntBus.on('set_customer_readonly', (value) => {
        this.readonly = value;
      });
      evntBus.on('set_customer_info_to_edit', (data) => {
        this.customer_info = data;
      });
      evntBus.on('fetch_customer_details', () => {
        this.get_customer_names();
      });
    });
  },

  watch: {
    customer() {
      evntBus.emit('update_customer', this.customer);
    },
  },
};
</script>
