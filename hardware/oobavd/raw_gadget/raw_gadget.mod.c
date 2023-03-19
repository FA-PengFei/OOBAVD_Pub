#include <linux/module.h>
#define INCLUDE_VERMAGIC
#include <linux/build-salt.h>
#include <linux/elfnote-lto.h>
#include <linux/vermagic.h>
#include <linux/compiler.h>

BUILD_SALT;
BUILD_LTO_INFO;

MODULE_INFO(vermagic, VERMAGIC_STRING);
MODULE_INFO(name, KBUILD_MODNAME);

__visible struct module __this_module
__section(".gnu.linkonce.this_module") = {
	.name = KBUILD_MODNAME,
	.init = init_module,
#ifdef CONFIG_MODULE_UNLOAD
	.exit = cleanup_module,
#endif
	.arch = MODULE_ARCH_INIT,
};

#ifdef CONFIG_RETPOLINE
MODULE_INFO(retpoline, "Y");
#endif

static const struct modversion_info ____versions[]
__used __section("__versions") = {
	{ 0x7d0b00ef, "module_layout" },
	{ 0x1993ee95, "no_llseek" },
	{ 0x3c9b3add, "misc_deregister" },
	{ 0xb3b172dd, "misc_register" },
	{ 0xaf201fa6, "usb_ep_enable" },
	{ 0x6cbbfc54, "__arch_copy_to_user" },
	{ 0xd6c0bd6b, "usb_gadget_vbus_draw" },
	{ 0x8732eef6, "usb_gadget_ep_match_desc" },
	{ 0xeedf1ba6, "usb_gadget_probe_driver" },
	{ 0x5a9f1d63, "memmove" },
	{ 0x6bd0e573, "down_interruptible" },
	{ 0x9ba909e4, "usb_gadget_set_state" },
	{ 0xdd64e639, "strscpy" },
	{ 0x9291cd3b, "memdup_user" },
	{ 0xdcb764ad, "memset" },
	{ 0xeb233a45, "__kmalloc" },
	{ 0x12a4e128, "__arch_copy_from_user" },
	{ 0x20000329, "simple_strtoul" },
	{ 0xa9e74462, "usb_ep_alloc_request" },
	{ 0xe2d5255a, "strcmp" },
	{ 0x296695f, "refcount_warn_saturate" },
	{ 0x5e2d7875, "cpu_hwcap_keys" },
	{ 0x14b89635, "arm64_const_caps_ready" },
	{ 0x7de1ffa7, "usb_gadget_unregister_driver" },
	{ 0xcf2a6966, "up" },
	{ 0x608741b5, "__init_swait_queue_head" },
	{ 0xfb42f7d6, "kmem_cache_alloc_trace" },
	{ 0x37a5fa8a, "kmalloc_caches" },
	{ 0xacfe2e7, "usb_ep_set_wedge" },
	{ 0xa8c3b4b, "usb_ep_set_halt" },
	{ 0x5fc294ef, "usb_ep_clear_halt" },
	{ 0x8da6585d, "__stack_chk_fail" },
	{ 0xdc88f81d, "_dev_err" },
	{ 0x25974000, "wait_for_completion" },
	{ 0x2e3bcce2, "wait_for_completion_interruptible" },
	{ 0x506ab3a9, "usb_ep_queue" },
	{ 0xa6257a2f, "complete" },
	{ 0xd35cce70, "_raw_spin_unlock_irqrestore" },
	{ 0x34db050b, "_raw_spin_lock_irqsave" },
	{ 0x882077d5, "usb_ep_dequeue" },
	{ 0x9eb52803, "usb_ep_disable" },
	{ 0x1b12bfb, "usb_ep_free_request" },
	{ 0x37a0cba, "kfree" },
};

MODULE_INFO(depends, "");


MODULE_INFO(srcversion, "CEBEA7C9908B8C5548E7B4F");
