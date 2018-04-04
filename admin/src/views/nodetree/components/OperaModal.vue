<template id='OperaModal'>
        <Modal v-model="openModal">
            <p slot="header" style="text-align:center">
                <Icon type="plus-round" v-if="currOpera==-1"></Icon>
                <Icon type="edit" v-if="currOpera!=-1"></Icon>
                <span v-if="currOpera==-1">新增</span>
                <span v-if="currOpera!=-1">编辑</span>
            </p>
            <div style="text-align:center">
                <Form ref="formObj" :model="formObj" :rules="ruleValidate" :label-width="80">
                    <FormItem label="Name" prop="Name">
                        <Input v-model="formObj.Name" placeholder="Please input this node name..."></Input>
                    </FormItem>
                    <FormItem label="IdentifyId" prop="IdentifyId">
                        <Input v-model="formObj.IdentifyId" placeholder="Please input this node identify number..."></Input>
                    </FormItem>
                    <FormItem label="Student" prop="is_Student">
                        <i-switch v-model="formObj.is_Student" size="large">
                            <span slot="open">是</span>
                            <span slot="close">否</span>
                        </i-switch>
                    </FormItem>
                    <div v-if="formObj.is_Student">
            	        <FormItem label="Patriarch Name" prop="pName">
            	            <Input v-model="formObj.pName" placeholder="Please input patriarch name..."></Input>
            	        </FormItem>
            	        <FormItem label="Patriarch Contact" prop="pContact">
            	            <Input v-model="formObj.pContact"  placeholder="Please input patriarch contact..."></Input>
            	        </FormItem>
            	       </div>
                </Form>
            </div>
            <div slot="footer">
                <Button type="success" size="default" :loading="loading"  @click.native= "formSubmit" :disabled="saveDisabled">保存</Button>
                <Button type="dashed" size="default" @click.native="formCancel">取消</Button>
            </div>
        </Modal>
</template>
<script>
	
    export default {
        name: 'OperaModal',
        props:{
                Name: String,
                IdentifyId: String,
                is_Student: Boolean,
                pName: String,
                pContact: String,
                openModal: Boolean,
                currOpera: Number,
                clearModalForm: Boolean
        },
        data (){
        	const getStudent	= ()=>{
        		return this.formObj.is_Student;
        	};
        	const checkPname 	= (rule, value, callback) => {
        		var student_status = getStudent()
        		if(student_status){
        			if(value === ''){
        				callback(new Error('Can not be empty'));
	        		}else if(value.length > 128){
	        			callback(new Error('More than of max length'));
	        		}else{
	        			callback();
	        		}
        		}else{
        			callback();
        		}
        		
        	};
        	const checkPcontact	= (rule, value, callback) => {
        		var student_status = getStudent()
				if(student_status){
					if(value === ''){
        				callback(new Error('Can not be empty'));
	        		}else if(value.length != 11){
	        			callback(new Error('Invalid phone number format'));
	        		}else if(/\d{11}$/.test(value) === false){
	        			callback(new Error('Invalid phone number format'));
	        		}else{
	        			callback();
	        		}
				}else{
					callback();
				}
        	};
            return {
                formObj: JSON.parse(JSON.stringify(this.formItem))
                checkret: true,
                saveDisabled: true,
                loading: false,
                ruleValidate: {
                    Name: [
                        { required: true, message: 'Can not be empty', trigger: 'blur' },
                        { max: 128, message: 'More than of max length', trigger: 'change'}
                    ],
                    IdentifyId: [
                        { required: true, message: 'Can not be empty', trigger: 'blur' },
                        { max: 60, message: 'More than of max length', trigger: 'change' }
                    ],
                    pName: [
                    	{ validator: checkPname, trigger: 'blur'}
                        
                    ],
                    pContact: [
                    	{ validator: checkPcontact, trigger: 'blur'}
                    ]
                }
            }
        },
        watch:{
            formObj:{
                handler (val) {
                	this.$refs.formObj.validate((valid) => {
                		if(valid){
                			this.saveDisabled = false
                		}else{
                			this.saveDisabled = true
                		}
                	})
                },
                deep: true
            },
            'formObj.is_Student': function(val){
            	if(val){
            		this.saveDisabled = true
            	}
            },
            clearModalForm: function(val){
                this.$refs.formObj.resetFields()
            }
        },
        methods:{
        	clearModal(){
        		this.checkret=true
                this.saveDisabled=true
                this.loading=false
        		this.$emit('closeModal', false)
        	},
            formSubmit(){
            	this.$emit('formBind', this.formObj)
            	this.loading = true
            	setTimeout(()=>{}, 2000)
             	this.$Message.info('save success')
             	this.clearModal()
            },
            formCancel(){
             	this.clearModal()
            }
        }
    }
</script>