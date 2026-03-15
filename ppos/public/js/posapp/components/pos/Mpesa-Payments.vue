<template>
  <v-row justify="center">
    <v-dialog v-model="dialog" max-width="800px" min-width="800px">
      <v-card>
        <v-card-title>
          <span class="headline text-primary">{{ __('Select Payment') }}</span>
        </v-card-title>
        <v-container>
          <v-row class="mb-4">
            <v-text-field
              color="primary"
              :label="frappe._('Full Name')"
              bg-color="white"
              hide-details
              v-model="full_name"
              density="compact"
              clearable
              class="mx-4"
            ></v-text-field>
            <v-text-field
              color="primary"
              :label="frappe._('Mobile No')"
              bg-color="white"
              hide-details
              v-model="mobile_no"
              density="compact"
              clearable
              class="mx-4"
            ></v-text-field>
            <v-btn variant="text" class="ml-2" color="primary" @click="search">{{
              __('Search')
            }}</v-btn>
          </v-row>
          <v-row>
            <v-col cols="12" class="pa-1" v-if="dialog_data">
              <v-data-table
                :headers="headers"
                :items="dialog_data"
                item-value="name"
                class="elevation-1"
                select-strategy="single"
                show-select
                v-model="selected"
              >
                <template v-slot:item.amount="{ item }">{{
                  formtCurrency(item.amount)
                }}</template>
                <template v-slot:item.posting_date="{ item }">{{
                  item.posting_date.slice(0, 16)
                }}</template>
              </v-data-table>
            </v-col>
          </v-row>
        </v-container>
        <v-card-actions class="mt-4">
          <v-spacer></v-spacer>
          <v-btn color="error" class="mx-2" @click="close_dialog">Close</v-btn>
          <v-btn
            v-if="selected.length"
            color="success"
            @click="submit_dialog"
            >{{ __('Submit') }}</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import { evntBus } from '../../bus';
export default {
  data: () => ({
    dialog: false,
    selected: [],
    dialog_data: '',
    company: '',
    customer: '',
    mode_of_payment: '',
    full_name: '',
    mobile_no: '',
    headers: [
      {
        title: __('Full Name'),
        value: 'full_name',
        align: 'start',
        sortable: true,
      },
      {
        title: __('Mobile No'),
        value: 'mobile_no',
        align: 'start',
        sortable: true,
      },
      {
        title: __('Amount'),
        value: 'amount',
        align: 'start',
        sortable: true,
      },
      {
        title: __('Date'),
        align: 'start',
        sortable: true,
        value: 'posting_date',
      },
    ],
  }),
  watch: {},
  methods: {
    close_dialog() {
      this.dialog = false;
    },
    search() {
      const vm = this;
      frappe.call({
        method: 'ppos.ppos.api.m_pesa.get_mpesa_draft_payments',
        args: {
          company: this.company,
          mode_of_payment: this.mode_of_payment,
          mobile_no: this.mobile_no,
          full_name: this.full_name,
        },
        async: false,
        callback: function (r) {
          if (!r.exc) {
            vm.dialog_data = r.message;
          }
        },
      });
    },
    submit_dialog() {
      const vm = this;
      if (this.selected.length > 0) {
        const selectedPayment = this.dialog_data.find(d => d.name === this.selected[0]);
        if (!selectedPayment) return;
        frappe.call({
          method: 'ppos.ppos.api.m_pesa.submit_mpesa_payment',
          args: {
            mpesa_payment: selectedPayment.name,
            customer: this.customer,
          },
          async: false,
          callback: function (r) {
            if (!r.exc) {
              evntBus.emit('set_mpesa_payment', r.message);
              vm.dialog = false;
            }
          },
        });
      }
    },
    formtCurrency(value) {
      value = parseFloat(value);
      return value.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
    },
  },
  created() {
    evntBus.on('open_mpesa_payments', (data) => {
      this.dialog = true;
      this.full_name = '';
      this.mobile_no = '';
      this.company = data.company;
      this.customer = data.customer;
      this.mode_of_payment = data.mode_of_payment;
      this.dialog_data = '';
      this.selected = [];
    });
  },
  beforeUnmount() {
    evntBus.off('open_mpesa_payments');
  },
};
</script>
