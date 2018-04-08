<template>
    <div>
        <Table :data="tableData1" :columns="tableColumns1" stripe></Table>
        <div style="margin: 10px;overflow: hidden">
            <div style="float: right;">
                <Page :total="totalPages" :current="currentPage" @on-change="changePage"></Page>
            </div>
        </div>
    </div>
</template>
<script>
    export default {
        name: 'OperaTable',
        data () {
            return {
                tableData1: this.mockTableData1(),
                tableColumns1: this.generateData(),
                totalPages: this.getTotalPages(),
                currentPage: this.getCurrentPage()
            }
        },
        methods: {
            mockTableData1 () {
            	let data = []
            	data.push({
            		name: '小明',
            		identify: '0101010101010101010101'
            	})
                return data;
            },
            changePage () {
                // The simulated data is changed directly here, and the actual usage scenario should fetch the data from the server
                this.tableData1 = this.mockTableData1();
            },
            generateData(type){
                let data = [
                    {
                        title: 'Name',
                        key: 'name'
                    },
                    {
                        title: 'Identify',
                        key: 'identify'
                    },
                    {
                        title: 'Operation',
                        key: 'operation',
                        fixed: 'right',
	                    width: 160,
	                    render: (h, params) => {
	                        return h('div', [
	                            h('Button', {
	                                props: {
	                                    type: 'ghost',
	                                    size: 'small',
	                                    icon: 'eye'
	                                }
	                            }, 'View'),
	                            h('Button', {
	                                props: {
	                                    type: 'ghost',
	                                    size: 'small',
	                                    icon: 'edit'
	                                }
	                            }, 'Edit')
	                        ]);
	                    }
                    }
                ]
                return data
            },
        	getTotalPages (){
        		return 1
        	},
        	getCurrentPage (){
        		return 1
        	}
        }
    }
</script>