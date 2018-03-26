<template>
	<Row type="flex" align="bottom" justify="center">
        <Col span="4">
        	<Tree :data="data1" :render="renderContent" ></Tree>
        </Col>
        <Col span="20">
        	<Page :total="100"></Page>
        </Col>
    </Row>
</template>
<script>
    export default {
        data () {
            return {
                data1: [
                    {
                        title: 'parent 1',
                        expand: true,
                        children: [
                            {
                                title: 'parent 1-1',
                                expand: true,
                                children: [
                                    {
                                        title: 'leaf 1-1-1'
                                    },
                                    {
                                        title: 'leaf 1-1-2'
                                    }
                                ]
                            },
                            {
                                title: 'parent 1-2',
                                expand: true,
                                children: [
                                    {
                                        title: 'leaf 1-2-1'
                                    },
                                    {
                                        title: 'leaf 1-2-1'
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        }
    }
</script>
<!--<script>
    export default {
        data () {
            return {
                modal5: false,
                data1: [
                    {
                        title: 'parent 1',
                        expand: false,
                        render: (h, {root, node, data}) => {
                            return h('span', {
                                style: {
                                    display: 'inline-block',
                                    width: '100%'
                                }
                            }, [h('span', [h('span', data.title)]),
                                h('span', {style: {display: 'inline-block', marginLeft: '24px'}}, [h('Button', {
                                    props: Object.assign({}, {
                                        type: 'text'
                                    }),
                                    style: {
                                        color: 'red'
                                    },
                                    on: {
                                        
                                        click: () => {
                                            alert(11);
                                        }
                                    }
                                }, '设置')])]);
                        },
                        children: [
                            {
                                title: 'parent 1-1',
                                expand: false,
                                children: [
                                    {
                                        title: 'leaf 1-1-1'
                                    },
                                    {
                                        title: 'leaf 1-1-2'
                                    }
                                ]
                            },
                            {
                                title: 'parent 1-2',
                                expand: false,
                                children: [
                                    {
                                        title: 'leaf 1-2-1'
                                    },
                                    {
                                        title: 'leaf 1-2-1'
                                    }
                                ]
                            }
                        ]
                    }
                ]
            };
        },
        methods: {
            renderContent (h, {root, node, data}) {
                return h('span', {
                    style: {
                        display: 'inline-block',
                        width: '100%'
                    }
                }, [
                    h('span', [
                        h('span', data.title)
                    ]),
                    h('span', {
                        style: {
                            display: 'inline-block',
                            marginLeft: '24px'
                        }
                    }, [
                        h('Button', {
                            props: Object.assign({}, {
                                type: 'text'
                            }),
                            style: {
                                color: 'red'
                            },
                            on: {
                                // 增加2级目录
                                click: () => {
                                    // this.append(data);
                                    alert(111);
                                }
                            }
                        }, '设置')
                    ])
                ]);
            }
        }
    };
</script>-->