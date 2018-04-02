<template>
    <Modal v-model="operModal">
        <p slot="header" style="text-align:center">
            <Icon type="plus-round" v-if="currOpera==-1"></Icon>
            <Icon type="edit" v-if="currOpera!=-1"></Icon>
            <span v-if="currOpera==-1">新增</span>
            <span v-if="currOpera!=-1">编辑</span>
        </p>
        <div style="text-align:center">
            <Form ref="formData" :model="formData" :rules="ruleValidate" :label-width="80">
                <FormItem label="Name" prop="Name" :error="nameState">
                    <Input v-model="formData.Name" @on-change="formBind" placeholder="Please input this node name..."></Input>
                </FormItem>
                <FormItem label="IdentifyId" prop="IdentifyId" :validateStatus="formStatus.identifyStatus">
                    <Input v-model="formData.IdentifyId" @on-change="formBind" placeholder="Please input this node identify number..."></Input>
                </FormItem>
                <FormItem label="Student" prop="is_Student">
                    <i-switch v-model="formData.is_Student" @on-change="formBind" size="large">
                        <span slot="open">是</span>
                        <span slot="close">否</span>
                    </i-switch>
                </FormItem>
                <div v-if="formData.is_Student">
        	        <FormItem label="Patriarch Name" prop="pName" :validateStatus="formStatus.pNameStatus">
        	            <Input v-model="formData.pName" @on-change="formBind" placeholder="Please input patriarch name..."></Input>
        	        </FormItem>
        	        <FormItem label="Patriarch Contact" prop="pContact" :validateStatus="formStatus.pContactStatus">
        	            <Input v-model="formData.pContact" @on-change="formBind"  placeholder="Please input patriarch contact..."></Input>
        	        </FormItem>
        	       </div>
            </Form>
        </div>
        <div slot="footer">
            <Button type="success" size="large" long :loading="loading"   @click.native= "formBind" :disabled="saveDisabled">
              保存
            </Button>
        </div>
    </Modal>
</template>
<script>
	
    export default {
        name: 'OperaModal',
        props:
        [
                'formData',
                'operModal',
                'currOpera'
        ],
        data () {
        	const getStudent	= ()=>{
        		return this.formData.is_Student;
        	}
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
                },
                nameState: '',
                formStatus: {
                	nameStatus: false,
                	identifyStatus: false,
                	pNameStatus: false,
                	pContactStatus: false
                }
            }
        },
        watch:{
            formData:{
                handler (val) {
//              	this.$Message.info(this.$refs['ruleForm2'].validate() ? "this is true" : "this is false")
                	this.$refs.formData.validate((valid) => {
                		if(valid){
                			this.saveDisabled = false
                		}else{
                			this.saveDisabled = true
                		}
                	})
                },
                deep: true
            },
            'formData.is_Student': function(val){
            	if(val){
            		this.saveDisabled = true
            	}
            }
        },
        methods:{
             checkData(name){
                
             }
        }
    }
</script>