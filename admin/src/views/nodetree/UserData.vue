<template>
    <div>
        <Row type="flex"  align="top" justify="center">
            <Col span="4">
                <OperaTree :Node="treeNode" @treeAdd="treeAdd"></OperaTree>
            </Col>
            <Col span="20">
                <!--<OperaTable></OperaTable>-->
                <can-edit-table v-model="tableData" :hoverShow="false" :editIncell="true" :columns-list="tableColumns"></can-edit-table>
            </Col>
        </Row>
        <opera-modal :openModal="openModal" :currOpera="currOpera" :formItem="formData" @closeModal="closeModal" @formBind="getMadolData"></opera-modal>
    </div>
</template>
<script>
    import OperaModal   from './components/OperaModal.vue'
    import OperaTable   from './components/OperaTable.vue'
    import OperaTree    from './components/OperaTree.vue'
    import canEditTable from './components/canEditTable.vue'
    export default {
        name: 'tree',
        components:{
            OperaModal,
            OperaTable,
            OperaTree,
            canEditTable
        },
        data () {
            return {
                operReady: false,
                openModal: false,
                currOpera: -1,
                formData: {
                    Name: '小明',
                    IdentifyId: '',
                    is_Student: false,
                    pName: '',
                    pContact: ''
                },
                treeNode: {},
                tableColumns: [
        		    {
        		    	title: 'Name',
        		    	key: 'Name',
        		    	editable: true
        		    },
        		    {
        		    	title: 'identify',
        		    	key: 'IdentifyId',
        		    	editable: true
        		    },
        		    {
        		    	title: '操作',
        		    	align: 'center',
        		    	width: 180,
        		    	key: 'handle',
        		    	handle: ['edit', 'delete']
    			    }
        		],
                tableData: []
            }
        },
        created () {
        	this.tableData = [
        		{
        			Name: '小明',
                    IdentifyId: '12121212121212121212',
                    is_Student: false,
                    pName: '小强',
                    pContact: '18192034329'
        		}
        	]
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
            },
            closeModal(value){
            	this.openModal 		= value
            },
            treeAdd(value){
                this.openModal 		= value
            }
        }
    }
</script>
