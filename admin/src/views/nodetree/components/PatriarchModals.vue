<template>
    <Form :model="formItem" :label-width="80">
        <FormItem label="Name">
            <Input v-model="formItem.Name" placeholder="Please input this node name..."></Input>
        </FormItem>
        <FormItem label="IdentifyId">
            <Input v-model="formItem.IdentifyId" placeholder="Please input this node identify number..."></Input>
        </FormItem>
        <FormItem label="Student">
            <i-switch v-model="formItem.is_Student" size="large">
                <span slot="open">是</span>
                <span slot="close">否</span>
            </i-switch>
        </FormItem>
        <div v-if="formItem.is_Student">
	        <FormItem label="Patriarch Name">
	            <Input v-model="formItem.Patriarch.pName" placeholder="Please input patriarch name..."></Input>
	        </FormItem>
	        <FormItem label="Patriarch Contact">
	            <Input v-model="formItem.Patriarch.pContact" placeholder="Please input patriarch contact..."></Input>
	        </FormItem>
	    </div>
    </Form>
</template>
<script>
    export default {
    	name: 'PatriarchModals',
        data () {
            return {
                formItem: {
                    Name: '',
                    IdentifyId: '',
                    is_Student: false,
                    Patriarch: {
                    	pName: '',
                    	pContact: ''
                    }
                }
            }
        }
    }
</script>