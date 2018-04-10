<template>
    <Tree :data="TreeData" :render="renderContent" @on-toggle-expand="GenerateData"></Tree>
</template>
<script>
    export default {
    	name: 'OperaTree',
    	props:
    	[
    		'Node'
    	],
        data () {
            return {
            	operaNode: Object,
                TreeData: [
                    {
                        title: 'parent 1',
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
                                            click: () => { this.verifyAdd(root, data, node) }
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
                }
            }
        },
        watch:{
        	Node:{
                handler (val) {
                	this.append()
                },
                deep: true
        	}
        },
        methods: {
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
                                click: () => { this.verifyAdd(root, node, data) }
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
            GenerateData(value){
            	let data = []
                for(var  key in value)
                {
                        if(key === "title"){
                            data.push({
                                    "Name": value[key],
                                    "IdentifyId": "01",
                                    "Property": true,
                                    "NodeKey" : value['nodeKey']})
                        }
                        if(key === "children"){
                            for(var key1 in value[key])
                            {
                                if(value[key][key1].title){
                                    data.push({
                                        "Name": value[key][key1].title,
                                        "IdentifyId": "02",
                                        "Property": false,
                                        "NodeKey" : value[key][key1].nodeKey})
                                }
                            }
                        }
                }
            	this.$emit('CheckOutData', data)
            	
            },
            verifyAdd (root, node, data) {
                this.operaNode = data
//              let tmp_node = JSON.stringify(data)
            	this.$emit('treeAdd', true)
            },
            append(){
            	if(this.operaNode){
            		const children = this.operaNode.children || [];
            		children.push({
	                    title: this.Node.Name,
	                    expand: true
                 	});
                 	this.$set(this.operaNode, 'children', children);
                 	this.operaNode = Object
            	}
            }
            ,
            remove (root, node, data) {
                const parentKey = root.find(el => el === node).parent;
                const parent = root.find(el => el.nodeKey === parentKey).node;
                const index = parent.children.indexOf(data);
                parent.children.splice(index, 1);
            }
        }
    }
</script>