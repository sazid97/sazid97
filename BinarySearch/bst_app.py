import streamlit as st
import graphviz


class TreeNode:
    def __init__(self, x):
        self.value = x
        self.left = None
        self.right = None


def insert(root, data):
    if root is None:
        return TreeNode(data)
    if root.value < data:
        root.right = insert(root.right, data)
    if root.value > data:
        root.left = insert(root.left, data)
    return root


def minValue(root):
    current = root
    while current.left:
        current = current.left
    return current.value

def print_order(root):
    return print_order(root.left) + [root.value] + print_order(root.right) if root else [] 


def delete(root, data):
    if not root:
        return None
    elif root.value < data:
        root.right = delete(root.right, data)
    elif root.value > data:
        root.left = delete(root.left, data)
    else:
        if not root.right:
            return root.left
        elif not root.left:
            return root.right
        temp = minValue(root.right)
        root.value = temp
        root.right = delete(root.right, temp)
    return root

def post_order(root):
    return root.left + root.right + [root.value] if root else None

def draw_tree(root):
    def add_nodes_edges(dot, node):
        if node.left:
            dot.node(str(node.left.value))  # ✅ define left node
            dot.edge(str(node.value), str(node.left.value))
            add_nodes_edges(dot, node.left)
        if node.right:
            dot.node(str(node.right.value))  # ✅ define right node
            dot.edge(str(node.value), str(node.right.value))
            add_nodes_edges(dot, node.right)

    dot = graphviz.Digraph()
    if root:
        dot.node(str(root.value))  # ✅ define root node
        add_nodes_edges(dot, root)
    return dot


st.title("Binary Search Tree Visualizer !!!")
if 'bst_root' not in st.session_state:
    st.session_state.bst_root = None
with st.form("insert_form"):
    insert_value = st.number_input("Insert a value: ", step=1, format="%d")
    insert_button = st.form_submit_button("Insert")
if insert_button:
    st.session_state.bst_root = insert(st.session_state.bst_root, insert_value)
    st.success(f"Inserted {insert_value}")

with st.form("delete_form"):
    delete_val = st.number_input("Delete a value", step=1, format="%d", key="delete")
    delete_button = st.form_submit_button("delete")

if delete_button:
    st.session_state.bst_root = delete(st.session_state.bst_root, delete_val)
    st.warning(f"Deleted {delete_val}")


inorder_result = print_order(st.session_state.bst_root)
st.subheader("In - order Traversal")
st.write(inorder_result if inorder_result else "tree is empty.")

post_order = post_order(st.session.bst_root)
st.subheader("Post order Traversal")
st.write(post_order if post_order else "Tree Is empty")

st.subheader("Tree Structure: ")
tree_graph = draw_tree(st.session_state.bst_root)
st.graphviz_chart(tree_graph)
