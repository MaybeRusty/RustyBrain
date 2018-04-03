<template>
    <div>
        <Row type="flex"  align="top" justify="center">
            <Col span="4">
                <OperaTree :Node="formData" @treeAdd="treeAdd"></OperaTree>
            </Col>
            <Col span="20">
                <OperaTable></OperaTable>
            </Col>
        </Row>
        <OperaModal :clearModalForm="clearModalForm" :openModal="openModal" :currOpera="currOpera" :formItem="formData" @closeModal="closeModal" @formBind="getMadolData"></OperaModal>
    </div>
</template>
<script>
    import OperaModal from './components/OperaModal.vue'
    import OperaTable from './components/OperaTable.vue'
    import OperaTree from './components/OperaTree.vue'
    export default {
        components:{
            OperaModal,
            OperaTable,
            OperaTree
        },
        data () {
            return {
                operReady: false,
                openModal: false,
                currOpera: -1,
                clearModalForm: false,
                formData: {
                    Name: '',
                    IdentifyId: '',
                    is_Student: false,
                    pName: '',
                    pContact: ''
                },
                treeNode: {
                    Name: '',
                    IdentifyId: '',
                    is_Student: false,
                    pName: '',
                    pContact: ''
                }
            }
        },
        watch:{
        	formData:{
        		handler (val){
        			this.$Message.info(this.formData.Name)
        		},
        		deep:true
        	}
        },
        methods: {
            getMadolData(value){
            	this.$Message.info("get modal data")
                this.formData = value
                this.treeNode = this.formData
                this.clearModalForm = true
            },
            closeModal(value){
                this.clearModalForm = false
            	this.openModal = value
            },
            treeAdd(value){
                this.openModal = value
            }
        }
    }
</script>
