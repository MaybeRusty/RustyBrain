<template>
    <div id="tree">
    <Row type="flex"  align="top" justify="center">
        <Col span="4">
        	<Tree :data="data1" :render="renderContent" @on-toggle-expand="setTreeNode"></Tree>
        </Col>
        <Col span="20">
            <Table :data="tableData1" :columns="tableColumns1" stripe></Table>
            <div style="margin: 10px;overflow: hidden">
                <div style="float: right;">
                    <Page :total="100" :current="current_page" @on-change="changePage"></Page>
                </div>
            </div>
        </Col>
    </Row>
    <OperaModal :operModal="operModal" :currOpera="currOpera" @formBind="getMadolData" :formData="formData"></OperaModal>
</div>
</template>
<script>
    import OperaModal from './components/OperaModal.vue'
    export default {
        name: "tree",
        data () {
            return {
                operReady: false,
                operModal: false,
                currOpera: -1,
            	current_page: 1,
                formData: {
        			Name: '',
        			IdentifyId: '',
        			is_Student: false,
        			Patriarch: {
        				pName: '',
        				pContact: ''
        			}
                },
            	data1: [
                    {
                        title: 'parent 1',
                        node_uuid: '123213321321312313213',
                        expand: false,
                        render: (h, { root, node, data }) => {
                            return h('span', {
                                style: {
                                    display: 'inline-block',
                                    width: '100%'
                                }
                            }, [
                                h('span', [
                                    h('Icon', {
                                        props: {
                                            type: 'ios-folder-outline'
                                        },
                                        style: {
                                            marginRight: '8px'
                                        }
                                    }),
                                    h('span', data.title)
                                ]),
                                h('span', {
                                    style: {
                                        display: 'inline-block',
                                        float: 'right',
                                        marginRight: '32px'
                                    }
                                }, [
                                    h('Button', {
                                        props: Object.assign({}, this.buttonProps, {
                                            icon: 'ios-plus-empty',
                                            type: 'primary'
                                        }),
                                        style: {
                                            width: '52px'
                                        },
                                        on: {
                                            click: () => { 
                                                this.operModal=true;
                                                this.$Message.info(this.operModal ? "true" : "false");
                                             }
                                        }
                                    })
                                ])
                            ]);
                        },
                        children: [
                            {
                                title: 'child 1-1',
                                expand: false,
                                children: [
                                    {
                                        title: 'leaf 1-1-1',
                                        expand: false
                                    },
                                    {
                                        title: 'leaf 1-1-2',
                                        expand: false
                                    }
                                ]
                            },
                            {
                                title: 'child 1-2',
                                expand: false,
                                children: [
                                    {
                                        title: 'leaf 1-2-1',
                                        expand: false
                                    },
                                    {
                                        title: 'leaf 1-2-1',
                                        expand: false
                                    }
                                ]
                            }
                        ]
                    }
                ],
                buttonProps: {
                    type: 'ghost',
                    size: 'small',
                },
                tableData1: this.mockTableData1(),
                tableColumns1: [
                    {
                        title: 'Name',
                        key: 'name'
                    },
                    {
                        title: 'Status',
                        key: 'status',
                        render: (h, params) => {
                            const row = params.row;
                            const color = row.status === 1 ? 'blue' : row.status === 2 ? 'green' : 'red';
                            const text = row.status === 1 ? 'Working' : row.status === 2 ? 'Success' : 'Fail';

                            return h('Tag', {
                                props: {
                                    type: 'dot',
                                    color: color
                                }
                            }, text);
                        }
                    },
                    {
                        title: 'Portrayal',
                        key: 'portrayal',
                        render: (h, params) => {
                            return h('Poptip', {
                                props: {
                                    trigger: 'hover',
                                    title: params.row.portrayal.length + 'portrayals',
                                    placement: 'bottom'
                                }
                            }, [
                                h('Tag', params.row.portrayal.length),
                                h('div', {
                                    slot: 'content'
                                }, [
                                    h('ul', this.tableData1[params.index].portrayal.map(item => {
                                        return h('li', {
                                            style: {
                                                textAlign: 'center',
                                                padding: '4px'
                                            }
                                        }, item)
                                    }))
                                ])
                            ]);
                        }
                    },
                    {
                        title: 'People',
                        key: 'people',
                        render: (h, params) => {
                            return h('Poptip', {
                                props: {
                                    trigger: 'hover',
                                    title: params.row.people.length + 'customers',
                                    placement: 'bottom'
                                }
                            }, [
                                h('Tag', params.row.people.length),
                                h('div', {
                                    slot: 'content'
                                }, [
                                    h('ul', this.tableData1[params.index].people.map(item => {
                                        return h('li', {
                                            style: {
                                                textAlign: 'center',
                                                padding: '4px'
                                            }
                                        }, item.n + '：' + item.c + 'People')
                                    }))
                                ])
                            ]);
                        }
                    },
                    {
                        title: 'Sampling Time',
                        key: 'time',
                        render: (h, params) => {
                            return h('div', 'Almost' + params.row.time + 'days');
                        }
                    },
                    {
                        title: 'Updated Time',
                        key: 'update',
                        render: (h, params) => {
                            return h('div', this.formatDate(this.tableData1[params.index].update));
                        }
                    }
                ]
            }
        },
        components:{
            OperaModal
        },
        methods: {
        	node2Table (current_node) {
        		let data = []
        		data.push({
        			name: current_node.title,
        			status: Math.floor(Math.random () * 3 + 1),
        			portrayal: ['City', 'People', 'Cost', 'Life', 'Entertainment'],
        			people: [
                            {
                                n: 'People' + Math.floor(Math.random () * 100 + 1),
                                c: Math.floor(Math.random () * 1000000 + 100000)
                            },
                            {
                                n: 'People' + Math.floor(Math.random () * 100 + 1),
                                c: Math.floor(Math.random () * 1000000 + 100000)
                            },
                            {
                                n: 'People' + Math.floor(Math.random () * 100 + 1),
                                c: Math.floor(Math.random () * 1000000 + 100000)
                            }
                        ],
                    time: Math.floor(Math.random () * 7 + 1),
                    update: new Date()
        		})
        		return data;
        	},
        	setTreeNode(payload) {
        		this.tableData1 = this.node2Table(payload);
        		this.current_page = 6
        	},
            mockTableData1 () {
                let data = [];
                for (let i = 0; i < 15; i++) {
                    data.push({
                        name: 'Business' + Math.floor(Math.random () * 100 + 1),
                        status: Math.floor(Math.random ()  * 3 + 1),
                        portrayal: ['City', 'People', 'Cost', 'Life', 'Entertainment'],
                        people: [
                            {
                                n: 'People' + Math.floor(Math.random () * 100 + 1),
                                c: Math.floor(Math.random () * 1000000 + 100000)
                            },
                            {
                                n: 'People' + Math.floor(Math.random () * 100 + 1),
                                c: Math.floor(Math.random () * 1000000 + 100000)
                            },
                            {
                                n: 'People' + Math.floor(Math.random () * 100 + 1),
                                c: Math.floor(Math.random () * 1000000 + 100000)
                            }
                        ],
                        time: Math.floor(Math.random () * 7 + 1),
                        update: new Date()
                    })
                }
                return data;
            },
            formatDate (date) {
                const y = date.getFullYear();
                let m = date.getMonth() + 1;
                m = m < 10 ? '0' + m : m;
                let d = date.getDate();
                d = d < 10 ? ('0' + d) : d;
                return y + '-' + m + '-' + d;
            },
            changePage () {
                // The simulated data is changed directly here, and the actual usage scenario should fetch the data from the server
                this.tableData1 = this.mockTableData1();
            },
            renderContent (h, { root, node, data }) {
                return h('span', {
                    style: {
                        display: 'inline-block',
                        width: '100%'
                    }
                }, [
                    h('span', [
                        h('Icon', {
                            props: {
                                type: 'ios-paper-outline'
                            },
                            style: {
                                marginRight: '8px'
                            }
                        }),
                        h('span', data.title)
                    ]),
                    h('span', {
                        style: {
                            display: 'inline-block',
                            float: 'right',
                            marginRight: '32px'
                        }
                    }, [
                        h('Button', {
                            props: Object.assign({}, this.buttonProps, {
                                icon: 'ios-plus-empty'
                            }),
                            style: {
                                marginRight: '8px'
                            },
                            on: {
                                click: () => { this.addNode() }
                            }
                        }),
                        h('Button', {
                            props: Object.assign({}, this.buttonProps, {
                                icon: 'ios-minus-empty'
                            }),
                            on: {
                                click: () => { this.remove(root, node, data) }
                            }
                        })
                    ])
                ]);
            },
            append (data) {
                const children = data.children || [];
                children.push({
                    title: 'appended node',
                    expand: true
                });
                this.$set(data, 'children', children);
            },
            remove (root, node, data) {
                const parentKey = root.find(el => el === node).parent;
                const parent = root.find(el => el.nodeKey === parentKey).node;
                const index = parent.children.indexOf(data);
                parent.children.splice(index, 1);
            },
            getMadolData(){
                this.formData = value
                this.$Message.success("save success!")
            }
        }
    }
</script>
