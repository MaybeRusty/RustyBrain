<template>
    <Form :model="formItem" :rules="ruleValidate" :label-width="80">
        <FormItem label="Name" prop="Name">
            <Input v-model="formItem.Name" @on-change="formBind" placeholder="Please input this node name..."></Input>
        </FormItem>
        <FormItem label="IdentifyId" prop="IdentifyId">
            <Input v-model="formItem.IdentifyId" @on-change="formBind" placeholder="Please input this node identify number..."></Input>
        </FormItem>
        <FormItem label="Student" prop="is_Student">
            <i-switch v-model="formItem.is_Student" @on-change="formBind" size="large">
                <span slot="open">是</span>
                <span slot="close">否</span>
            </i-switch>
        </FormItem>
        <div v-if="formItem.is_Student">
	        <FormItem label="Patriarch Name" prop="pName">
	            <Input v-model="formItem.pName" @on-change="formBind" placeholder="Please input patriarch name..."></Input>
	        </FormItem>
	        <FormItem label="Patriarch Contact" prop="pContact">
	            <Input v-model="formItem.pContact" @on-change="formBind"  placeholder="Please input patriarch contact..."></Input>
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
                    pName: '',
                    pContact: ''
                },
                ruleValidate: {
                    Name: [
                        { required: true, max: 3, message: 'The name cannot be empty', trigger: 'change' }
                    ],
                    IdentifyId: [
                        { required: true, max: 60, message: 'The Id cannot be empty', trigger: 'blur' },
                        { type: 'string', message: 'Must be string format', trigger: 'blur' }
                    ],
                    pContact: [
                    	{ type: 'string', len: 11, message: 'Must be phone number', trigger: 'change', pattern: /\d{11}$/}
                    ]
                }
            }
        },
        methods:{
             formBind: function(){
                this.$emit('formBind', this.formItem)
             }
        }
    }
</script>