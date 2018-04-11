<template>
    <div>
        <Row type="flex"  align="top" justify="center">
            <Col span="4">
                <OperaTree :updateTree="updateTree" :deleteTree="deleteTree" :Node="treeNode" @treeAdd="treeAdd" @CheckOutData="GenerateData"></OperaTree>
            </Col>
            <Col span="20">
                <!--<OperaTable></OperaTable>-->
                <can-edit-table v-model="tableData" :hoverShow="false" :editIncell="true" :columns-list="tableColumns" @on-change="ChangeTableData" @on-cell-change="ChangeTableCol"></can-edit-table>
            </Col>
        </Row>
        <opera-modal :openModal="openModal" :currOpera="currOpera" :formItem="formData" @closeModal="closeModal" @formBind="ChangeTableRow"></opera-modal>
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
        		    	title: '名称',
        		    	key: 'Name',
        		    	editable: true
        		    },
        		    {
        		    	title: '身份识别码',
        		    	key: 'IdentifyId',
        		    	editable: true
        		    },
        		    {
        		    	title: '管理节点',
        		    	key: 'Property',
        		    	render: (h, params) => {
                            const row = params.row;
                            const color = row.Property === true ? 'blue' : 'green';
                            const text = row.Property === true ? 'Manager' : 'Member';

                            return h('Tag', {
                                props: {
                                    type: 'dot',
                                    color: color
                                }
                            }, text);
                        },
        		    	editable: false
        		    },
        		    {
        		    	title: '操作',
        		    	align: 'center',
        		    	width: 180,
        		    	key: 'handle',
        		    	handle: ['edit', 'delete']
    			    }
        		],
                tableData:  [],
                updateTree: {},
                deleteTree: {}
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
            },
            closeModal(value){
            	this.openModal 		= value
            },
            treeAdd(value){
                this.openModal 		= value
            },
            GenerateData(value){
            	this.tableData  = value
            },
            ChangeTableRow(value, index){
            	this.updateTree = value[index]
            },
            ChangeTableCol(value, index, key){
            	this.updateTree = value[index]
            }
        }
    }
</script>
