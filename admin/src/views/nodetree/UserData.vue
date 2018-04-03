<template>
    <div>
        <Row type="flex"  align="top" justify="center">
            <Col span="4">
                <OperaTree :Node="treeNode" @treeAdd="treeAdd"></OperaTree>
            </Col>
            <Col span="20">
                <OperaTable></OperaTable>
            </Col>
        </Row>
        <opera-modal :clearModalForm="clearModalForm" :openModal="openModal" :currOpera="currOpera" v-bind="formData" @closeModal="closeModal" @formBind="getMadolData"></opera-modal>
    </div>
</template>
<script>
    import OperaModal from './components/OperaModal.vue'
    import OperaTable from './components/OperaTable.vue'
    import OperaTree from './components/OperaTree.vue'
    export default {
        name: 'tree',
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
                treeNode: {}
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
                this.treeNode = value
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
