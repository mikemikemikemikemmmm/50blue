<template>
    <tr>
        <td>{{ orderData.created_at }}</td>
        <td>{{ orderData.total_price }}</td>
        <td>
            <v-icon v-if="!isShowDetail" class="me-2" size="small" @click="handleClickShowDetail">
                mdi-arrow-down-drop-circle-outline
            </v-icon>
            <v-icon v-else class="me-2" size="small" @click="handleClickShowDetail">
                mdi-arrow-up-drop-circle-outline
            </v-icon>
        </td>
        <td></td>
        <td></td>
        <td></td>
        <td> <v-icon size="small" @click="handleDelete">
                mdi-delete
            </v-icon></td>
    </tr>
    <template v-if="isShowDetail">
        <tr v-for="orderItem in orderData.order_items">
            <td></td>
            <td>{{ orderItem.price }}</td>
            <td>{{ orderItem.drink_name }}</td>
            <td>{{ orderItem.ice_content }}</td>
            <td>{{ orderItem.sugar_content }}</td>
            <td>{{ formatOrderItemToppingList(orderItem.topping_name_list) }}</td>
            <td></td>

        </tr>
    </template>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { OrderApi } from '../../api';
import { formatOrderItemToppingList } from '../../utils';
const isShowDetail = ref(false)
const props = defineProps<{ orderData: OrderApi.GetResponse }>()
const emit = defineEmits<{
    (event: 'handle-delete-order', payload: { id: number }): void;
}>();

const handleDelete = () => {
    emit('handle-delete-order', { id: orderData.id });
}
const { orderData } = props
const handleClickShowDetail = () => {
    isShowDetail.value = !isShowDetail.value
}
</script>