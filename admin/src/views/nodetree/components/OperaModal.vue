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
                <FormItem label="Name" prop="Name">
                    <Input v-model="formData.Name" @on-change="formBind" placeholder="Please input this node name..."></Input>
                </FormItem>
                <FormItem label="IdentifyId" prop="IdentifyId">
                    <Input v-model="formData.IdentifyId" @on-change="formBind" placeholder="Please input this node identify number..."></Input>
                </FormItem>
                <FormItem label="Student" prop="is_Student">
                    <i-switch v-model="formData.is_Student" @on-change="formBind" size="large">
                        <span slot="open">是</span>
                        <span slot="close">否</span>
                    </i-switch>
                </FormItem>
                <div v-if="formData.is_Student">
        	        <FormItem label="Patriarch Name" prop="pName">
        	            <Input v-model="formData.pName" @on-change="formBind" placeholder="Please input patriarch name..."></Input>
        	        </FormItem>
        	        <FormItem label="Patriarch Contact" prop="pContact">
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
                        { required: true , message: 'Can not be empty', trigger: 'change'},
                        { max: 128, message: 'More than of max length', trigger: 'change'}
                    ],
                    pContact: [
                    	{ required: true , message: 'Must be phone number', trigger: 'change', pattern: /\d{11}$/},
                        { len: 11, message: 'invalid phone number', trigger: 'change'}
                    ]
                }
            }
        },
        watch:{
            formData:{
                handler (val) {
                    this.$Message.info(Object.values(val)[0])
                   //  for (let i = 0; i < Object.values(val).length; i++) {
                   //      Object.values(val)[i].validate((valid) => {
                   //          if (valid) {
                   //              this.saveDisabled = false
                   //          } else {
                   //              this.saveDisabled = true
                   //          }
                   //      })
                   // }
                    // this.$Message.info(this.saveDisabled ? "true" : "false")
                    this.$refs['formData'].validate((valid) => {
                        if (valid) {
                            this.saveDisabled = false
                        } else {
                            this.saveDisabled = true
                        }
                    })
                },
                deep: true
            }
        },
        methods:{
             checkData(name){
                
             }
        }
    }
</script>